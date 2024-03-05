from django.urls import path, include
from .views import (
    activity_view,
    causes_views,
    company_views,
    event_t_views,
    installation_views,
    province_views,
    state_views,
    structure_t_views,
    structure_views,
    work_t_views,
    work_view,
)

urlpatterns = [
    # Activity Nature
    path(
        "activity-nature/",
        activity_view.Activity_Nature_ApiOverview,
        name="activity-nature-overview",
    ),
    path(
        "activity-nature/all",
        activity_view.View_Activity_Nature,
        name="activity-nature-all",
    ),
    path(
        "activity-nature/create",
        activity_view.Add_Activity_Nature,
        name="activity-nature-create",
    ),
    path(
        "activity-nature/update/<str:pk>",
        activity_view.Update_Activity_Nature,
        name="activity-nature-update",
    ),
    path(
        "activity-nature/view/<str:pk>",
        activity_view.View_Activity_Nature,
        name="activity-nature-view",
    ),
    path(
        "activity-nature/delete/<str:pk>",
        activity_view.Delete_Activity_Nature,
        name="activity-nature-delete",
    ),
    # Causes
    path("causes/", causes_views.Cause_ApiOverview, name="causes-overview"),
    path("causes/create", causes_views.Add_Cause, name="causes-create"),
    path("causes/update/<str:pk>", causes_views.Update_Cause, name="causes-update"),
    path("causes/delete/<str:pk>", causes_views.Delete_Cause, name="causes-delete"),
    path("causes/view/<str:pk>", causes_views.View_Cause, name="causes-view"),
    path("causes/all", causes_views.View_Causes, name="causes-all"),
    # Company
    path("company/", company_views.Company_ApiOverview, name="company-overview"),
    path("company/all", company_views.View_Company, name="company-all"),
    path("company/create", company_views.Add_Company, name="company-create"),
    path(
        "company/update/<str:pk>", company_views.Update_Company, name="company-update"
    ),
    path("company/view/<str:pk>", company_views.View_Company, name="company-view"),
    path(
        "company/delete/<str:pk>", company_views.Delete_Company, name="company-delete"
    ),
    # Event Type
    path(
        "event-type/", event_t_views.Event_Type_ApiOverview, name="event-type-overview"
    ),
    path("event-type/create", event_t_views.Add_Event_Type, name="event-type-create"),
    path("event-type/all", event_t_views.View_Event_Types, name="event-type-all"),
    path(
        "event-type/update/<str:pk>",
        event_t_views.Update_Event_Type,
        name="event-type-update",
    ),
    path(
        "event-type/view/<str:pk>",
        event_t_views.View_Event_Type,
        name="event-type-view",
    ),
    path(
        "event-type/delete/<str:pk>",
        event_t_views.Delete_Event_Type,
        name="event-type-delete",
    ),
    # Installation
    path(
        "installation/",
        installation_views.Installation_ApiOverview,
        name="installation-overview",
    ),
    path(
        "installation/all",
        installation_views.View_Installations,
        name="installation-all",
    ),
    path(
        "installation/create",
        installation_views.Add_Installation,
        name="installation-create",
    ),
    path(
        "installation/update/<str:pk>",
        installation_views.Update_Installation,
        name="installation-update",
    ),
    path(
        "installation/view/<str:pk>",
        installation_views.View_Installation,
        name="installation-view",
    ),
    path(
        "installation/delete/<str:pk>",
        installation_views.Delete_Installation,
        name="installation-delete",
    ),
    # Province
    path("province/", province_views.Province_ApiOverview, name="province-overview"),
    path("province/all", province_views.View_Provinces, name="province-all"),
    path("province/create", province_views.Add_Province, name="province-create"),
    path(
        "province/update/<str:pk>",
        province_views.Update_Province,
        name="province-update",
    ),
    path("province/view/<str:pk>", province_views.View_Province, name="province-view"),
    path(
        "province/delete/<str:pk>",
        province_views.Delete_Province,
        name="province-delete",
    ),
    # State
    path("state/", state_views.State_ApiOverview, name="state-overview"),
    path("state/all", state_views.View_States, name="state-all"),
    path("state/create", state_views.Add_State, name="state-create"),
    path("state/update/<str:pk>", state_views.Update_State, name="state-update"),
    path("state/view/<str:pk>", state_views.View_State, name="state-view"),
    path("state/delete/<str:pk>", state_views.Delete_State, name="state-delete"),
    # Structure Type
    path(
        "structure-type/",
        structure_t_views.Structure_Type_ApiOverview,
        name="structure-type-overview",
    ),
    path(
        "structure-type/all",
        structure_t_views.View_Structure_Types,
        name="structure-type-all",
    ),
    path(
        "structure-type/create",
        structure_t_views.Add_Structure_Type,
        name="structure-type-create",
    ),
    path(
        "structure-type/update/<str:pk>",
        structure_t_views.Update_Structure_Type,
        name="structure-type-update",
    ),
    path(
        "structure-type/view/<str:pk>",
        structure_t_views.View_Structure_Type,
        name="structure-type-view",
    ),
    path(
        "structure-type/delete/<str:pk>",
        structure_t_views.Delete_Structure_Type,
        name="structure-type-delete",
    ),
    # Structure
    path(
        "structure/", structure_views.Structure_ApiOverview, name="structure-overview"
    ),
    path("structure/all", structure_views.View_Structures, name="structure-all"),
    path("structure/create", structure_views.Add_Structure, name="structure-create"),
    path(
        "structure/update/<str:pk>",
        structure_views.Update_Structure,
        name="structure-update",
    ),
    path(
        "structure/view/<str:pk>", structure_views.View_Structure, name="structure-view"
    ),
    path(
        "structure/delete/<str:pk>",
        structure_views.Delete_Structure,
        name="structure-delete",
    ),
    # Work Type
    path("work-type/", work_t_views.Work_Type_ApiOverview, name="work-type-overview"),
    path("work-type/all", work_t_views.View_Work_Types, name="work-type-all"),
    path("work-type/create", work_t_views.Add_Work_Type, name="work-type-create"),
    path(
        "work-type/update/<str:pk>",
        work_t_views.Update_Work_Type,
        name="work-type-update",
    ),
    path("work-type/view/<str:pk>", work_t_views.View_Work_Type, name="work-type-view"),
    path(
        "work-type/delete/<str:pk>",
        work_t_views.Delete_Work_Type,
        name="work-type-delete",
    ),
    # Work
    path("work/", work_view.Work_ApiOverview, name="work-overview"),
    path("work/all", work_view.View_Work, name="work-all"),
    path("work/create", work_view.Add_Work, name="work-create"),
    path("work/update/<str:pk>", work_view.Update_Work, name="work-update"),
    path("work/view/<str:pk>", work_view.View_Work, name="work-view"),
    path("work/delete/<str:pk>", work_view.Delete_Work, name="work-delete"),
]
