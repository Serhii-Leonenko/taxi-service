from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CarForm, DriverCreationForm, DriverLicenseUpdateForm, CarSearchForm
from .models import Driver, Car, Manufacturer


@login_required
def index(request):
    """View function for the home page of the site."""

    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": num_visits + 1,
    }

    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 3


class ManufacturerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")


class ManufacturerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")


class ManufacturerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Manufacturer
    success_url = reverse_lazy("taxi:manufacturer-list")


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 3
    queryset = Car.objects.all().select_related("manufacturer")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CarListView, self).get_context_data(**kwargs)

        model = self.request.GET.get("model", "")

        context["search_form"] = CarSearchForm(
            initial={
                "model": model
            }
        )

        return context

    def get_queryset(self):
        form = CarSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                model__icontains=form.cleaned_data["model"]
            )


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarForm


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    form_class = CarForm


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")


def car_add_driver_view(request, pk):
    Car.objects.get(pk=pk).drivers.add(request.user)
    return HttpResponseRedirect(reverse("taxi:car-detail", kwargs={'pk': pk}))


def car_delete_driver_view(request, pk):
    Car.objects.get(pk=pk).drivers.remove(request.user)
    return HttpResponseRedirect(reverse("taxi:car-detail", kwargs={'pk': pk}))


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 3


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.all().prefetch_related("cars__manufacturer")


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = Driver
    form_class = DriverCreationForm


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    success_url = reverse_lazy("taxi:driver-list")


class DriverLicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "taxi/driver_license_form.html"
    model = Driver
    form_class = DriverLicenseUpdateForm
