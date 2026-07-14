from django.contrib import admin
from .models import (
    HQ, DailyProductionData, Factory, Department, FactoryStructure, HanContent, HanTrainingContent, LevelThreeQualitySubStation, LevelTwoQualitySubStation, Line, Level, Days,
    EmployeeMaster, LineStructure, MultiSkilling, NewDepartment, NewFactory, NewLine, NewWorkstation, RefreshmentTraining, Score, ShoContent, ShoTrainingContent, ShopFloor, Station, OperatorSkill, StationStructure, TestSession, TrainingReport, TrainingTopic, OperatorTraining,
    MonthlyAssignment, OperatorLevelTracking, OperatorLevelEmailTracking, TrackingEmail,
    Machine, MachineAllocation, MachineAllocationTrackingEmail,
    SkillTraining, SubTopic, SubTopicContent, TrainingContent,
    LevelTwoProduction, LevelTwoLine, LevelTwoSubStation, EmployeeLevelAssignment,
    LevelTwoTraineeInfo, LevelTwoTrainingTopic, LevelTwoOJTDay, LevelTwoOJTScore,
    LevelTwoQuality, LevelTwoQualityLine, LevelTwoQATraineeInfo,
    LevelTwoQATrainingTopic, LevelTwoQAOJTDay, LevelTwoQAOJTScore,
    LevelThreeProduction, LevelThreeLine, LevelThreeSubStation,
    LevelThreeTraineeInfo, LevelThreeTrainingTopic, LevelThreeOJTDay, LevelThreeOJTScore,
    LevelThreeQuality, LevelThreeQualityLine, LevelThreeQATraineeInfo,
    LevelThreeQATrainingTopic, LevelThreeQAOJTDay, LevelThreeQAOJTScore,
    ARVRTrainingContent, MCQQuestion, BiometricAttendance, UnifiedDefectReport
)

# Basic registrations
admin.site.register(HQ)
admin.site.register(Factory)
admin.site.register(Department)
admin.site.register(Line)
# admin.site.register(Level)

from django.contrib import admin
from .models import Level


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ("id", "line", "name", "get_display_name")
    list_filter = ("line", "name")
    search_fields = ("line__name", "name")
    ordering = ("line", "name")
    list_per_page = 25

    def get_display_name(self, obj):
        return obj.get_name_display()
    get_display_name.short_description = "Level"

admin.site.register(Days)

# admin.site.register(EmployeeMaster)

from django.contrib import admin
from .models import EmployeeMaster


@admin.register(EmployeeMaster)
class EmployeeMasterAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "pay_code",
        "card_no",
        "name",
        "department",
        "section",
        "desig_category",
        "joining_date",
        "auth_shift",
        "shift_type",
        "shift_pattern",
        "first_weekly_off",
        "second_weekly_off",
        "ot_allowed_rate",
        "round_the_clock",
    )
    list_filter = (
        "department",
        "section",
        "desig_category",
        "sex",
        "auth_shift",
        "shift_type",
        "shift_pattern",
        "ot_allowed_rate",
        "round_the_clock",
    )
    search_fields = (
        "pay_code",
        "card_no",
        "name",
        "guardian_name",
        "department",
        "section",
        "desig_category",
    )
    ordering = ("name",)
    list_per_page = 25

admin.site.register(Station)
admin.site.register(OperatorSkill)
admin.site.register(TrainingTopic)
admin.site.register(OperatorTraining)
admin.site.register(MonthlyAssignment)

admin.site.register(OperatorLevelTracking)
admin.site.register(OperatorLevelEmailTracking)
admin.site.register(TrackingEmail)

admin.site.register(NewFactory)
admin.site.register(NewDepartment)
admin.site.register(NewLine)
admin.site.register(NewWorkstation)


admin.site.register(FactoryStructure)
admin.site.register(ShopFloor)
admin.site.register(LineStructure)
admin.site.register(StationStructure)

admin.site.register(DailyProductionData)







admin.site.register(Machine)
admin.site.register(MachineAllocation)
admin.site.register(MachineAllocationTrackingEmail)

admin.site.register(SkillTraining)
admin.site.register(SubTopic)
admin.site.register(SubTopicContent)
admin.site.register(TrainingContent)

admin.site.register(LevelTwoProduction)
admin.site.register(LevelTwoLine)
admin.site.register(LevelTwoSubStation)
admin.site.register(EmployeeLevelAssignment)

admin.site.register(LevelTwoTraineeInfo)
admin.site.register(LevelTwoTrainingTopic)
admin.site.register(LevelTwoOJTDay)
admin.site.register(LevelTwoOJTScore)

admin.site.register(LevelTwoQuality)
admin.site.register(LevelTwoQualityLine)
admin.site.register(LevelTwoQATraineeInfo)
admin.site.register(LevelTwoQATrainingTopic)
admin.site.register(LevelTwoQAOJTDay)
admin.site.register(LevelTwoQAOJTScore)

admin.site.register(LevelThreeProduction)
admin.site.register(LevelThreeLine)
admin.site.register(LevelThreeSubStation)

admin.site.register(LevelThreeTraineeInfo)
admin.site.register(LevelThreeTrainingTopic)
admin.site.register(LevelThreeOJTDay)
admin.site.register(LevelThreeOJTScore)

admin.site.register(LevelThreeQuality)
admin.site.register(LevelThreeQualityLine)
admin.site.register(LevelThreeQATraineeInfo)
admin.site.register(LevelThreeQATrainingTopic)
admin.site.register(LevelThreeQAOJTDay)
admin.site.register(LevelThreeQAOJTScore)

admin.site.register(ARVRTrainingContent)
admin.site.register(MCQQuestion)
admin.site.register(BiometricAttendance)


admin.site.register(MultiSkilling)
admin.site.register(RefreshmentTraining)


admin.site.register(TrainingReport)
admin.site.register(UnifiedDefectReport)


admin.site.register(Score)
admin.site.register(TestSession)



admin.site.register(HanContent)
admin.site.register(HanTrainingContent)
admin.site.register(ShoContent)
admin.site.register(ShoTrainingContent)


admin.site.register(LevelTwoQualitySubStation)

admin.site.register(LevelThreeQualitySubStation)



from django.contrib import admin
from .models import QuestionPaper, Question

@admin.register(QuestionPaper)
class QuestionPaperAdmin(admin.ModelAdmin):
    list_display = ('name','id')
    search_fields = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'question_paper', 'correct_index')
    list_filter = ('question_paper',)
    search_fields = ('question_text',)


from django.contrib import admin
from .models import MainDepartment, MainLine, SubLine

# Inline for SubLine (Third level)
class SubLineInline(admin.TabularInline):
    model = SubLine
    extra = 1

# Inline for MainLine (Second level)
class MainLineInline(admin.TabularInline):
    model = MainLine
    extra = 1

# Admin for MainDepartment with inline MainLine
class MainDepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [MainLineInline]

# Admin for MainLine with inline SubLine
class MainLineAdmin(admin.ModelAdmin):
    list_display = ['name', 'department']
    list_filter = ['department']
    inlines = [SubLineInline]

# Admin for SubLine
class SubLineAdmin(admin.ModelAdmin):
    list_display = ['name', 'main_line']
    list_filter = ['main_line']

# Register all
admin.site.register(MainDepartment, MainDepartmentAdmin)
admin.site.register(MainLine, MainLineAdmin)
admin.site.register(SubLine, SubLineAdmin)


from django.contrib import admin
from .models import UploadedFile

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_at']




from .models import User
admin.site.register(User)







from django.contrib import admin
from .models import ManagementReview

@admin.register(ManagementReview)
class ManagementReviewAdmin(admin.ModelAdmin):
    list_display = (
        'month_year',
        'new_operators_joined',
        'new_operators_trained',
        'total_training_plans',
        'total_trainings_actual',
        'total_defects_msil',
        'ctq_defects_msil',
        'total_defects_tier1',
        'ctq_defects_tier1',
        'total_internal_rejection',
        'ctq_internal_rejection',
    )
    list_filter = ('month_year',)
    search_fields = ('month_year',)
    ordering = ('-month_year',)




from .models import UserInfo,HumanBodyCheck


admin.site.register(UserInfo)
admin.site.register(HumanBodyCheck)








from django.contrib import admin
from .models import (
    Training_category,
    Curriculum,
    CurriculumContent,
    Trainer_name,
    Venues,
    Schedule,
    EmployeeAttendance,
    RescheduleLog
)


class CurriculumInline(admin.TabularInline):
    model = Curriculum
    extra = 1


@admin.register(Training_category)
class TrainingCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at")
    search_fields = ("name",)
    inlines = [CurriculumInline]


class CurriculumContentInline(admin.TabularInline):
    model = CurriculumContent
    extra = 1


@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ("topic", "category", "created_at")
    search_fields = ("topic", "category__name")
    list_filter = ("category",)
    inlines = [CurriculumContentInline]


@admin.register(CurriculumContent)
class CurriculumContentAdmin(admin.ModelAdmin):
    list_display = ("content_name", "content_type", "curriculum", "uploaded_at")
    search_fields = ("content_name", "curriculum__topic")
    list_filter = ("content_type",)


@admin.register(Trainer_name)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Venues)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class EmployeeAttendanceInline(admin.TabularInline):
    model = EmployeeAttendance
    extra = 0


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "training_category",
        "training_name",
        "trainer",
        "venue",
        "status",
        "date",
        "time",
    )
    list_filter = ("status", "training_category", "trainer", "venue", "date")
    search_fields = ("training_name__topic", "trainer__name", "venue__name")
    filter_horizontal = ("employees",)
    inlines = [EmployeeAttendanceInline]


@admin.register(EmployeeAttendance)
class EmployeeAttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "schedule",
        "status",
        "reschedule_date",
        "reschedule_time",
        "updated_at",
    )
    list_filter = ("status", "reschedule_date")
    search_fields = ("employee__first_name", "employee__last_name", "schedule__training_name__topic")


@admin.register(RescheduleLog)
class RescheduleLogAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "schedule",
        "original_date",
        "original_time",
        "new_date",
        "new_time",
        "reason",
        "created_at",
    )
    list_filter = ("new_date", "original_date")
    search_fields = ("employee__first_name", "employee__last_name", "schedule__training_name__topic")


from .models import NewMultiSkilling

admin.site.register(NewMultiSkilling)


