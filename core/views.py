from django.shortcuts import render
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, TemplateView

from .models import Radiograph
from .filters import RadiographFilter

from django_filters.views import FilterView


class FilteredRadiographListView(FilterView, ListView):
    model = Radiograph
    template_name= "core/radiograph_list.html"
    context_object_name = "items"
    ordering = ["-created"]
    filterset_class = RadiographFilter


class RadiographCreateView(CreateView):
    model = Radiograph
    fields = ["img", "age", "sex"]
    success_url = "/"


class RadiographUpdateView(UpdateView):
    model = Radiograph
    fields = ["img", "age", "sex", ]
    success_url = "/"


class RadiographDeleteView(DeleteView):
    model = Radiograph
    success_url = "/"


class TrainingAnalysisView(TemplateView):
    template_name = "core/training.html"


class DashboardView(TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        queryset = Radiograph.objects.all()

        # chart 1
        labels = []
        data = []
        
        normal_diagnosis = Radiograph.objects.filter(reading="0")
        normal_diagnosis_count = normal_diagnosis.count()
        tb_diagnosis = Radiograph.objects.filter(reading="1")
        tb_diagnosis_count = tb_diagnosis.count()

        labels = [
            "Normal",
            "Tuberculosis",
            ]

        data = [normal_diagnosis_count, tb_diagnosis_count]

        # chart 2
        labels2 = []
        data2 = []

        normal_diagnosis_male = Radiograph.objects.filter(reading="0").filter(sex="0")
        normal_diagnosis_count_male = normal_diagnosis_male.count()
        tb_diagnosis_male = Radiograph.objects.filter(reading="1").filter(sex="0")
        tb_diagnosis_count_male = tb_diagnosis_male.count()
        normal_diagnosis_female = Radiograph.objects.filter(reading="0").filter(sex="1")
        normal_diagnosis_count_female = normal_diagnosis_female.count()
        tb_diagnosis_female = Radiograph.objects.filter(reading="1").filter(sex="1")
        tb_diagnosis_count_female = tb_diagnosis_female.count()

        labels2 = [
            "Normal Male",
            "Normal Female",
            "Tuberculosis Male", 
            "Tuberculosis Female", 
            ]

        data2 = [normal_diagnosis_count_male, normal_diagnosis_count_female, tb_diagnosis_count_male, tb_diagnosis_count_female]


        # chart 3
        labels3 = []
        data3 = []

        one = Radiograph.objects.filter(reading="0").filter(age__lte=19)
        one = one.count()
        two = Radiograph.objects.filter(reading="0").filter(age__lte=29).filter(age__gte=20)
        two = two.count()
        three = Radiograph.objects.filter(reading="0").filter(age__lte=39).filter(age__gte=30)
        three = three.count()
        four = Radiograph.objects.filter(reading="0").filter(age__lte=49).filter(age__gte=40)
        four = four.count()
        five = Radiograph.objects.filter(reading="0").filter(age__lte=59).filter(age__gte=50)
        five = five.count()
        six = Radiograph.objects.filter(reading="0").filter(age__lte=69).filter(age__gte=60)
        six = six.count()
        seven = Radiograph.objects.filter(reading="0").filter(age__lte=79).filter(age__gte=70)
        seven = seven.count()
        eight = Radiograph.objects.filter(reading="0").filter(age__lte=89).filter(age__gte=80)
        eight = eight.count()
        nine = Radiograph.objects.filter(reading="0").filter(age__gte=99)
        nine = nine.count()

        labels3 = [
            "0-19 years old",
            "Twenties",
            "Thirties", 
            "Fourties", 
            "Fifties", 
            "Sixties", 
            "Seventies", 
            "Eighties", 
            "Nineties", 
            "Greater that 99 years old", 
            ]

        data3 = [ one, two, three, four, five, six, seven, eight, nine ]

        # chart 4
        labels4 = []
        data4 = []

        one_pos = Radiograph.objects.filter(reading="1").filter(age__lte=19)
        one_pos = one_pos.count()
        two_pos = Radiograph.objects.filter(reading="1").filter(age__lte=29).filter(age__gte=20)
        two_pos = two_pos.count()
        three_pos = Radiograph.objects.filter(reading="1").filter(age__lte=39).filter(age__gte=30)
        three_pos = three_pos.count()
        four_pos = Radiograph.objects.filter(reading="1").filter(age__lte=49).filter(age__gte=40)
        four_pos = four_pos.count()
        five_pos = Radiograph.objects.filter(reading="1").filter(age__lte=59).filter(age__gte=50)
        five_pos = five_pos.count()
        six_pos = Radiograph.objects.filter(reading="1").filter(age__lte=69).filter(age__gte=60)
        six_pos = six_pos.count()
        seven_pos = Radiograph.objects.filter(reading="1").filter(age__lte=79).filter(age__gte=70)
        seven_pos = seven_pos.count()
        eight_pos = Radiograph.objects.filter(reading="1").filter(age__lte=89).filter(age__gte=80)
        eight_pos = eight_pos.count()
        nine_pos = Radiograph.objects.filter(reading="1").filter(age__gte=99)
        nine_pos = nine_pos.count()

    
        labels4 = [
            "0-19 years old",
            "Twenties",
            "Thirties", 
            "Fourties", 
            "Fifties", 
            "Sixties", 
            "Seventies", 
            "Eighties", 
            "Nineties", 
            "Greater that 99 years old", 
            ]

        data4 = [ one_pos, two_pos, three_pos, four_pos, five_pos, six_pos, seven_pos, eight_pos, nine_pos ]


        context.update({
            "labels": labels,
            "data": data,
            "labels2": labels2,
            "data2": data2,
            "labels3": labels3,
            "data3": data3,
            "labels4": labels4,
            "data4": data4,
        })
        return context
