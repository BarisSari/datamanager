from django.contrib import admin
from django.views.generic import TemplateView
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from budgetportal import models

from adminsortable.admin import SortableAdmin, SortableTabularInline
from budgetportal.bulk_upload import bulk_upload_view
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db.utils import ProgrammingError
from django.contrib import messages
from import_export.admin import ImportMixin
from import_export.formats.base_formats import CSV, XLSX
import logging

from .import_export_admin import (
    DepartmentResource,
    DepartmentImportForm,
    InfrastructureProjectResource,
)
import prov_infra_projects


logger = logging.getLogger(__name__)
admin.site.login = login_required(admin.site.login)


class FinancialYearAdmin(admin.ModelAdmin):
    pass


class SphereAdmin(admin.ModelAdmin):
    readonly_fields = ("slug",)


class GovernmentAdmin(admin.ModelAdmin):
    readonly_fields = ("slug",)


class GovtFunctionAdmin(admin.ModelAdmin):
    readonly_fields = ("slug",)


class InfrastructureProjectAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = InfrastructureProjectResource
    formats = [CSV]


class DepartmentAdmin(ImportMixin, admin.ModelAdmin):
    # Resource class to be used by the django-import-export package
    resource_class = DepartmentResource
    # File formats that can be used to import departments
    formats = [CSV]

    def get_import_form(self):
        """
        Get the import form to use by the django-import-export package
        to import departments.
        """
        return DepartmentImportForm

    def get_resource_kwargs(self, request, *args, **kwargs):
        """
        Get the kwargs to send on to the department resource when
        we import departments.
        """
        if u"sphere" in request.POST:
            return {"sphere": request.POST[u"sphere"]}
        return {}

    list_display = (
        "vote_number",
        "name",
        "get_government",
        "get_sphere",
        "get_financial_year",
    )
    list_display_links = ("vote_number", "name")
    list_filter = (
        "government__sphere__financial_year__slug",
        "government__sphere__name",
        "government__name",
    )
    search_fields = (
        "government__sphere__financial_year__slug",
        "government__sphere__name",
        "government__name",
        "name",
    )
    readonly_fields = ("slug",)
    list_per_page = 20

    def get_government(self, obj):
        return obj.government.name

    def get_sphere(self, obj):
        return obj.government.sphere.name

    def get_financial_year(self, obj):
        return obj.government.sphere.financial_year.slug


class ProgrammeAdmin(admin.ModelAdmin):
    list_display = (
        "programme_number",
        "name",
        "get_department",
        "get_government",
        "get_sphere",
        "get_financial_year",
    )
    list_display_links = ("programme_number", "name")
    list_filter = (
        "department__government__sphere__financial_year__slug",
        "department__government__sphere__name",
        "department__government__name",
        "department__name",
    )
    search_fields = (
        "department__government__sphere__financial_year__slug",
        "department__government__sphere__name",
        "department__government__name",
        "department__name",
        "name",
    )
    readonly_fields = ("slug",)

    def get_department(self, obj):
        return obj.department.name

    def get_government(self, obj):
        return obj.department.government.name

    def get_sphere(self, obj):
        return obj.department.government.sphere.name

    def get_financial_year(self, obj):
        return obj.department.government.sphere.financial_year.slug


class EntityDatasetsView(TemplateView):
    template_name = "admin/entity_datasets.html"
    financial_year_slug = None
    sphere_slug = None

    def get_context_data(self, **kwargs):
        sphere = models.Sphere.objects.get(
            financial_year__slug=self.financial_year_slug, slug=self.sphere_slug
        )
        return {"sphere": sphere}


class UserAdmin(admin.ModelAdmin):
    pass


class SiteAdmin(admin.ModelAdmin):
    pass


class VideoLanguageInline(SortableTabularInline):
    model = models.VideoLanguage


class VideoAdmin(SortableAdmin):
    inlines = [VideoLanguageInline]
    model = models.Video


class IRMSnapshotAdmin(admin.ModelAdmin):
    pass


class ProvInfraProjectSnapshotInline(admin.TabularInline):
    model = models.ProvInfraProjectSnapshot
    fields = ["name", "province", "department", "status", "irm_snapshot"]
    readonly_fields = fields


class ProvInfraProjectAdmin(admin.ModelAdmin):
    model = models.ProvInfraProject
    inlines = [ProvInfraProjectSnapshotInline]
    readonly_fields = ["IRM_project_id"]
    list_filter = (
        "project_snapshots__irm_snapshot",
        "project_snapshots__province",
        "project_snapshots__department",
    )
    search_fields = ("project_snapshots__name", "project_snapshots__project_number")


class ProvInfraProjectSnapshotAdmin(admin.ModelAdmin):
    list_display = ("name", "project_number", "province", "department", "irm_snapshot")
    list_display_links = ("name", "project_number")
    list_filter = ("irm_snapshot__financial_year__slug", "province", "department")
    search_fields = ("name", "project_number")
    list_per_page = 20

    def get_readonly_fields(self, request, obj=None):
        return list(
            set(
                [field.name for field in self.opts.local_fields]
                + [field.name for field in self.opts.local_many_to_many]
            )
        )


admin.site.register_view("bulk_upload", "Bulk Upload", view=bulk_upload_view)


try:
    for financial_year in models.FinancialYear.objects.all():
        for sphere in financial_year.spheres.all():
            view = EntityDatasetsView.as_view(
                financial_year_slug=financial_year.slug, sphere_slug=sphere.slug
            )
            path = "%s/%s/entity_datasets" % (financial_year.slug, sphere.slug)
            label = "Entity Datasets - %s %s" % (financial_year.slug, sphere.name)
            admin.site.register_view(path, label, view=view)
except ProgrammingError as e:
    logging.error(e, exc_info=True)


admin.site.register(models.FinancialYear, FinancialYearAdmin)
admin.site.register(models.Sphere, SphereAdmin)
admin.site.register(models.Government, GovernmentAdmin)
admin.site.register(models.GovtFunction, GovtFunctionAdmin)
admin.site.register(models.Department, DepartmentAdmin)
admin.site.register(models.InfrastructureProjectPart, InfrastructureProjectAdmin)
admin.site.register(models.Programme, ProgrammeAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(models.Video, VideoAdmin)
admin.site.register(models.Event)
admin.site.register(models.FAQ, SortableAdmin)
admin.site.register(models.ProvInfraProject, ProvInfraProjectAdmin)
admin.site.register(models.ProvInfraProjectSnapshot, ProvInfraProjectSnapshotAdmin)
admin.site.register(models.IRMSnapshot, IRMSnapshotAdmin)
admin.site.register(models.Homepage, admin.ModelAdmin)
