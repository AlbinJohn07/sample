from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from .views import ActiveTrainingBatchListView, BatchAttendanceDetailView, BulkAttendanceUpdateView, CompleteTrainingBatchView, CurriculumContentViewSet, CurriculumViewSet, DailyProductionDataViewSet, DepartmentByFactoryView, EmployeeAttendanceViewSet, FactoryStructureViewSet, FileDownloadView, GetThreeQATraineeByCodeView, GroupedLevelThreeScoreByEmployeeView, GroupedScoreByEmployeeView, HanContentViewSet, HanSubtopicViewSet, HanTrainingContentViewSet, HanchouExamQuestionViewSet, HanchouExamResultViewSet, HanchouResultCertificatePDF, LevelOneEmployeesView, LevelThreeOJTReportPDFView, LevelThreeOJTStatusViewSet, LevelThreeQAReportPDFView, LevelThreeQualitySubStationViewSet, LevelTwoOJTReportPDFView, LevelTwoQAReportPDFView, LevelTwoQualitySubStationViewSet, MachineAllocationApprovalViewSet, ManpowerCTQTrendsView, NewAdvancedManpowerCTQViewSet, NewDepartmentViewSet, NewFactoryViewSet, NewLineViewSet, NewWorkstationViewSet, NotificationViewSet, OJTStatusViewSet, OperatorRequirementViewSet, OperatorSkillCertificatePDF, PastTrainingBatchListView, ProductionPlanViewSet, RescheduleLogViewSet, SDCOrientationFeedbackViewSet, ScheduleViewSet, ScoreCertificatePDF, ShoSubtopicViewSet, ShokuchouExamQuestionViewSet, ShokuchouExamResultViewSet, ShokuchouResultCertificatePDF, SkillMatrixExcelView, SubmitWebTestAPIView, Trainer_nameViewSet, Training_categoryViewSet, UploadAdvancedManpowerCTQView, UploadedFileListView, VenueViewSet, dojo_app,UploadOperatorSkillsAPIView, get_plan_data, get_plan_other, get_plan_totals, serve_han_material_file, serve_sho_material_file


from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from .views import (
    notification_count,
    create_system_notification,
    create_test_notification,
    test_notifications,
    trigger_employee_notification,
    trigger_all_notification_types,
    delete_all_notifications,

    ARVRTrainingContentViewSet,LogoView, AllEmployeesWithActiveSkillsView, AllEmployeesWithCompletedSkillsView, AllEmployeesWithRescheduledSkillsView, BiometricAttendanceViewSet, CTQDefectsAllPlantsView, CardEmployeeDetailByNameView, CompanyLogoViewSet, DaysViewSet, DepartmentViewSet, EmployeeCardDetailsView, EmployeeExcelUploadView, EmployeeExcelViewSet, EmployeeMachineAllocationViewSet,  EmployeeNameByCodeAPIView, ExcelUploadFromPathView, ExcelUploadView, FactoryViewSet, GetLevelThreeTraineeByCodeView, GetQATraineeByCodeView,GetTraineeByCodeView, GroupedEmployeeSkillsView, HQViewSet, InternalRejectionView, LevelThreeLineViewSet, LevelThreeOJTDayViewSet, LevelThreeOJTScoreViewSet, LevelThreeProductionViewSet, LevelThreeQAOJTDayViewSet, LevelThreeQAOJTScoreViewSet, LevelThreeQATraineeInfoViewSet, LevelThreeQATrainingTopicViewSet, LevelThreeQualityLineViewSet, LevelThreeQualityViewSet, LevelThreeSubStationViewSet, LevelThreeTraineeInfoViewSet, LevelThreeTrainingTopicViewSet, LevelTwoLineViewSet, LevelTwoOJTDayViewSet, LevelTwoOJTScoreViewSet, LevelTwoProductionViewSet, LevelTwoQAOJTDayViewSet, LevelTwoQAOJTScoreViewSet, LevelTwoQATraineeInfoViewSet, LevelTwoQATrainingTopicViewSet, LevelTwoQualityLineViewSet, LevelTwoQualityViewSet, LevelTwoSubStationViewSet, LevelTwoTraineeInfoViewSet, LevelTwoTrainingTopicViewSet, LevelViewSet, LineViewSet, MCQBySubtopicView, MCQQuestionViewSet, MSILDefectsView, MachineAllocationViewSet, MachineViewSet, MainDepartmentListView, MainLinesByDepartmentView, MultiSkillingByEmployeeView, NestedLevelThreeQATraineeInfoViewSet, NestedLevelThreeTraineeInfoViewSet, NestedLevelTwoQATraineeInfoViewSet, NestedLevelTwoTraineeInfoViewSet, NewMultiSkillingViewSet, OperatorSkillByNameView, OperatorsJoinedVsTrainedView, RefreshmentTrainingByNameView, ScoreByEmployeeNameView, ShoContentViewSet,ShoTrainingContentViewSet, SkillTrainingViewSet, StationViewSet, OperatorSkillViewSet, StationsBySubLineView, SubLinesByMainLineView, SubTopicContentViewSet, SubTopicDayViewSet, SubTopicViewSet, SubtopicWiseTrainingContentViewSet, TrainingContentCreateView, TrainingContentViewSet, TrainingReportViewSet, TrainingSummaryView,EmployeeReportPDFView,
    TrainingTopicViewSet,DefectsChartView,TrainingPlansChartView,OperatorsChartView,CurrentMonthDefectsDataView,CurrentMonthTrainingDataView, ManagementReviewViewSet,ManagementReviewUploadView, OperatorTrainingViewSet, MonthlyAssignmentViewSet, UnifiedDefectReportViewSet, create_rescheduled_multiskilling, get_today_email_milestones, get_today_milestones,StationDeleteView,StationUpdateView,SetAttendanceTaskTimeView,SetManagementReviewTaskTimeView,SetAdvancedManpowerTaskTimeView,PreviousMonthDefectsDataView,NextMonthDefectsDataView
)

from .views import(
    UserInfoListCreateView,HumanBodyCheckListCreateView,PassedUsersWithDetailsView,AllPassedUsersView,UserInfoBodyCheckListView,RemainingDepartmentsView,UserInfoUpdateView
)

router = DefaultRouter()

router.register(r'notifications', NotificationViewSet, basename='notifications')
router.register(r'employees', views.EmployeeViewSet)
# router.register(r'operators', OperatorViewSet)
router.register(r'stations', StationViewSet)
router.register(r'operator-skills', OperatorSkillViewSet)
router.register(r'training-topics', TrainingTopicViewSet)
router.register(r'operator-trainings', OperatorTrainingViewSet)
router.register(r'monthly-assignments', MonthlyAssignmentViewSet)




router.register(r'hq', HQViewSet)
router.register(r'factories', FactoryViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'lines', LineViewSet)
router.register(r'levels', LevelViewSet)





router.register(r'skill-trainings', SkillTrainingViewSet)
router.register(r'subtopics', SubTopicViewSet)
router.register(r'subtopics-day', SubTopicDayViewSet, basename='subtopics-day')
router.register(r'subtopic-contents', SubTopicContentViewSet)
router.register(r'days', DaysViewSet)
router.register(r'training-contents', TrainingContentViewSet)



router.register(r'productions', LevelTwoProductionViewSet)
router.register(r'leveltwo-lines', LevelTwoLineViewSet)
router.register(r'substations', LevelTwoSubStationViewSet)
router.register(r'leveltwo-trainees', LevelTwoTraineeInfoViewSet)
router.register(r'leveltwo-topics', LevelTwoTrainingTopicViewSet)
router.register(r'leveltwo-days', LevelTwoOJTDayViewSet)
router.register(r'leveltwo-scores', LevelTwoOJTScoreViewSet)
router.register(r'level2-trainees-score', NestedLevelTwoTraineeInfoViewSet, basename='level2-trainee-score')




router.register(r'leveltwo-quality', LevelTwoQualityViewSet)
router.register(r'leveltwo-quality-lines', LevelTwoQualityLineViewSet)
router.register(r'leveltwo-quality-substation', LevelTwoQualitySubStationViewSet)
router.register(r'qa-trainees', LevelTwoQATraineeInfoViewSet)
router.register(r'qa-training-topics', LevelTwoQATrainingTopicViewSet)
router.register(r'qa-ojt-days', LevelTwoQAOJTDayViewSet)
router.register(r'qa-ojt-scores', LevelTwoQAOJTScoreViewSet)
router.register(r'nested-qa-trainees', NestedLevelTwoQATraineeInfoViewSet, basename='level2-qa-trainee-score')

router.register(r'level-three-productions', LevelThreeProductionViewSet)
router.register(r'level-three-lines', LevelThreeLineViewSet)
router.register(r'level-three-substations', LevelThreeSubStationViewSet)
router.register(r'levelthree-trainees', LevelThreeTraineeInfoViewSet)
router.register(r'levelthree-topics', LevelThreeTrainingTopicViewSet)
router.register(r'levelthree-days', LevelThreeOJTDayViewSet)
router.register(r'levelthree-scores', LevelThreeOJTScoreViewSet)
router.register(r'levelthree-trainees-score', NestedLevelThreeTraineeInfoViewSet,basename='level3-trainee-score')


router.register(r'level-three-quality', LevelThreeQualityViewSet)
router.register(r'level-three-quality-line', LevelThreeQualityLineViewSet)
router.register(r'level-three-qa-trainees', LevelThreeQATraineeInfoViewSet)
router.register(r'level-three-qa-topics', LevelThreeQATrainingTopicViewSet)
router.register(r'level-three-qa-days', LevelThreeQAOJTDayViewSet)
router.register(r'level-three-qa-scores', LevelThreeQAOJTScoreViewSet)
router.register(r'nested-level-three-qa-trainees', NestedLevelThreeQATraineeInfoViewSet,basename='level3-qatrainee-score')
router.register(r'levelthree-quality-substation', LevelThreeQualitySubStationViewSet)

router.register(r'machines', MachineViewSet, basename='machine')
router.register(r'machine-allocations', MachineAllocationViewSet, basename='machineallocation')






router.register(r'arvr-content', ARVRTrainingContentViewSet, basename='arvr-content')



router.register(r'mcqquestions', MCQQuestionViewSet)

router.register(r'biometric-attendance', BiometricAttendanceViewSet, basename='biometric-attendance')


router.register(r'newmultiskilling', NewMultiSkillingViewSet, basename='newmultiskilling')#post Multiskill

router.register(r'training-reports', TrainingReportViewSet)
router.register(r'unified-defect-reports', UnifiedDefectReportViewSet)
router.register(r'subtopicwisetrainingcontent', SubtopicWiseTrainingContentViewSet, basename='subtopicwisetrainingcontent')


router.register(r'employees-machine-allocations', EmployeeMachineAllocationViewSet, basename='employeemachineallocation')


router.register(r'management-review', ManagementReviewViewSet, basename='management-review')


# hanshou & shokuchou 

router.register(r'hanchou-questions', HanchouExamQuestionViewSet, basename='hanchou-questions')
router.register(r"hanchou/results", HanchouExamResultViewSet, basename="hanchou-results")

router.register(r"shokuchou-questions", ShokuchouExamQuestionViewSet, basename="shokuchou-questions")
router.register(r"shokuchou/results", ShokuchouExamResultViewSet, basename="shokuchou-results")


router.register(r'han-content', HanContentViewSet, basename='han-content')
router.register(r'han-subtopics', HanSubtopicViewSet,  basename='han-subtopic') 
router.register(r'han-materials', HanTrainingContentViewSet, basename='han-material')

router.register(r'sho-content', ShoContentViewSet, basename='sho-content')
router.register(r'sho-subtopics', ShoSubtopicViewSet, basename='sho-subtopic')
router.register(r'sho-materials', ShoTrainingContentViewSet, basename='sho-material')








router.register(r'employees-excel', EmployeeExcelViewSet, basename='employee-excel')
router.register(r'machine-allocation-approval', MachineAllocationApprovalViewSet, basename='machineallocationapproval')

router.register(r'advanced-ctq', NewAdvancedManpowerCTQViewSet, basename='advanced-ctq')
router.register(r'operator-requirements', OperatorRequirementViewSet)

router.register(r'logos', CompanyLogoViewSet)

# # Refreshment Training
router.register(r'training-categories', Training_categoryViewSet)
router.register(r'curriculums', CurriculumViewSet, basename='curriculum')
router.register(r'curriculum-contents', CurriculumContentViewSet, basename='curriculumcontent')
router.register(r'trainer_name', Trainer_nameViewSet)
router.register(r'venues', VenueViewSet)
router.register(r'schedules', ScheduleViewSet)
router.register(r'empattendances', EmployeeAttendanceViewSet, basename='attendance')
router.register(r'reschedule-logs', RescheduleLogViewSet, basename='reschedulelog')
# # multiskiiling
# router.register(r'multiskilling', MultiSkillingViewSet)
router.register(r'sdc-feedback', SDCOrientationFeedbackViewSet, basename='sdc-feedback')


# ---------------ojtlist urls------------------#
router.register(r"ojt-status", OJTStatusViewSet, basename="ojtstatus")
router.register(r"level3/ojt-status", LevelThreeOJTStatusViewSet, basename="level3ojtstatus")




router.register(r'new-multi-skilling', NewMultiSkillingViewSet, basename='new-multi-skilling')




router.register(r'factory-structures', FactoryStructureViewSet)

router.register(r'production-plans', ProductionPlanViewSet)

router.register(r'production-data', DailyProductionDataViewSet, basename='productiondata')


router.register(r'factory', NewFactoryViewSet)
router.register(r'department', NewDepartmentViewSet)
router.register(r'line', NewLineViewSet)
router.register(r'workstations', NewWorkstationViewSet)


urlpatterns = [
    path('', dojo_app),

    # Authentication routes
    path('', TemplateView.as_view(template_name='index.html')),
    
    # Main application routes
    
    path('home/', TemplateView.as_view(template_name='index.html')),
    path('management/', TemplateView.as_view(template_name='index.html')),
    path('advance/', TemplateView.as_view(template_name='index.html')),
    path('skillmatrix/', TemplateView.as_view(template_name='index.html')),
    
    # Form routes
    path('form/', TemplateView.as_view(template_name='index.html')),
    path('DownloadFiles/', TemplateView.as_view(template_name='index.html')),
    path('demo/', TemplateView.as_view(template_name='index.html')),
    path('demo1/', TemplateView.as_view(template_name='index.html')),
    path('ObservationForm/', TemplateView.as_view(template_name='index.html')),
    path('MESSummary/', TemplateView.as_view(template_name='index.html')),
    path('WasteDetails/', TemplateView.as_view(template_name='index.html')),
    path('methodsettings/', TemplateView.as_view(template_name='index.html')),
    path('MasterTable/', TemplateView.as_view(template_name='index.html')),
    path('training/', TemplateView.as_view(template_name='index.html')),
    
    # User management routes
    path('user/', TemplateView.as_view(template_name='index.html')),
    path('OperatorLogin/', TemplateView.as_view(template_name='index.html')),
    path('OperatorDashboard/', TemplateView.as_view(template_name='index.html')),
    path('QuestionsList/', TemplateView.as_view(template_name='index.html')),
    path('EvaluationTable/', TemplateView.as_view(template_name='index.html')),
    path('Evaluation/', TemplateView.as_view(template_name='index.html')),
    path('ProcessDojo/', TemplateView.as_view(template_name='index.html')),
    path('dojo/<str:name>/', TemplateView.as_view(template_name='index.html')),
    path('level1/<int:id>/', TemplateView.as_view(template_name='index.html')),
    
    # Training routes
    path('level-training/', TemplateView.as_view(template_name='index.html')),
    path('level-training/<str:level>/', TemplateView.as_view(template_name='index.html')),
    path('lesson-details/<int:id>/', TemplateView.as_view(template_name='index.html')),
    path('dojoTraining/', TemplateView.as_view(template_name='index.html')),
    path('PersonnelObservanceSheet/', TemplateView.as_view(template_name='index.html')),
    path('EmployeeSkillTraining/', TemplateView.as_view(template_name='index.html')),
    path('lvl2/', TemplateView.as_view(template_name='index.html')),
    path('level1/2', TemplateView.as_view(template_name='index.html')),
    path('level1/1', TemplateView.as_view(template_name='index.html')),
    path('level1/3', TemplateView.as_view(template_name='index.html')),
    path('QRScannerPage/', TemplateView.as_view(template_name='index.html')),
    path('lvl2/section/<int:sectionId>/', TemplateView.as_view(template_name='index.html')),
    path('lvl2/section/<int:sectionId>/subheading/<int:subheadingId>/', TemplateView.as_view(template_name='index.html')),
    path('tencycle/', TemplateView.as_view(template_name='index.html')),
    path('retrain/', TemplateView.as_view(template_name='index.html')),
    path('Level2OjtTable/', TemplateView.as_view(template_name='index.html')),
    path('Level2OjtQualityTable/', TemplateView.as_view(template_name='index.html')),
    
    # Level 3 routes
    path('Level3OjtTable/', TemplateView.as_view(template_name='index.html')),
    path('Level3OjtQualityTable/', TemplateView.as_view(template_name='index.html')),
    
    # Level-specific routes
    path('Level3/', TemplateView.as_view(template_name='index.html')),
    path('Level4/', TemplateView.as_view(template_name='index.html')),
    path('Level1/', TemplateView.as_view(template_name='index.html')),
    path('Level1/<int:id>/', TemplateView.as_view(template_name='index.html')),
    path('lvl2/subtopics/<int:topicId>/', TemplateView.as_view(template_name='index.html')),
    path('lvl2/units/<str:text>/<int:id>/', TemplateView.as_view(template_name='index.html')),
    path('level2/<int:id>/', TemplateView.as_view(template_name='index.html')),
    path('Hanchou/', TemplateView.as_view(template_name='index.html')),
    path('Shokuchou/', TemplateView.as_view(template_name='index.html')),
    path('ArVrComponent/', TemplateView.as_view(template_name='index.html')),
    path('notification/', TemplateView.as_view(template_name='index.html')),
    path('uploadMasterTable/', TemplateView.as_view(template_name='index.html')),
    path('SearchBar/', TemplateView.as_view(template_name='index.html')),
    
    # Machine and allocation routes
    #path('machines/', TemplateView.as_view(template_name='index.html')),
    #path('machine-allocations/', TemplateView.as_view(template_name='index.html')),
    path('approvallist/', TemplateView.as_view(template_name='index.html')),
    path('quiz/', TemplateView.as_view(template_name='index.html')),
    
    # Scheduling routes
    path('allocation/', TemplateView.as_view(template_name='index.html')),
    path('scheduling/', TemplateView.as_view(template_name='index.html')),
    path('refreshment/', TemplateView.as_view(template_name='index.html')),
    path('rescheduling/', TemplateView.as_view(template_name='index.html')),
    
    # Reporting routes
    path('biometric/', TemplateView.as_view(template_name='index.html')),
    path('report/', TemplateView.as_view(template_name='index.html')),
    path('EmployeeHistorySearch/', TemplateView.as_view(template_name='index.html')),
    
    # Remote quiz routes
    path('remote/', TemplateView.as_view(template_name='index.html')),
    path('add-question/', TemplateView.as_view(template_name='index.html')),
    path('assign-remote/', TemplateView.as_view(template_name='index.html')),
    path('quiz-results/', TemplateView.as_view(template_name='index.html')),
    path('quiz-instructions/', TemplateView.as_view(template_name='index.html')),
    path('UnderDevelopment/', TemplateView.as_view(template_name='index.html')),
    path('test-ended/', TemplateView.as_view(template_name='index.html')),





    path('attendance/', TemplateView.as_view(template_name='index.html')),
    path('ojt-statuse/', TemplateView.as_view(template_name='index.html')),
    path('SkillMatrix/', TemplateView.as_view(template_name='index.html')),
    path('advanced/', TemplateView.as_view(template_name='index.html')),
    path('planning/', TemplateView.as_view(template_name='index.html')),
    path('plan/', TemplateView.as_view(template_name='index.html')),
    path('planlist/', TemplateView.as_view(template_name='index.html')),



    path('Level0/', TemplateView.as_view(template_name='index.html')),
    path('TempEmployeeSearch/', TemplateView.as_view(template_name='index.html')),
    path('PassedUsersTable/', TemplateView.as_view(template_name='index.html')),
    path('attendance/', TemplateView.as_view(template_name='index.html')),
    path('ExamModeSelector/', TemplateView.as_view(template_name='index.html')),
    # path('machine-allocations/', TemplateView.as_view(template_name='index.html')),
    # path('machines/', TemplateView.as_view(template_name='index.html')),
    
    
    
    
   

    

    path('register/', views.RegisterView.as_view(), name="register"),
    # path('upload-operator-skills/', upload_operator_skills, name='upload-operator-skills'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', views.LogoutAPIView.as_view(), name="logout"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('trainingcontent/create/', TrainingContentCreateView.as_view(), name='trainingcontent-create'),
    path('milestone/alerts/', get_today_milestones, name='milestone-alerts'),
    path('milestone/email/alerts/', get_today_email_milestones, name='email_milestone-alerts'),


    path('trainee/<str:trainee_id>/<int:station_id>/', GetTraineeByCodeView.as_view(), name='get_trainee_by_code_station'),
    path('qa-trainee/<str:trainee_id>/<int:station_id>/', GetQATraineeByCodeView.as_view(), name='get_qa_trainee_by_code'),


    path('levelthree-trainee/<str:trainee_id>/<int:station_id>/', GetLevelThreeTraineeByCodeView.as_view(), name='get_levelthree_trainee'),
    path('qa-trainees/<str:trainee_id>/<int:station_id>/', GetThreeQATraineeByCodeView.as_view(), name='get_qa_trainee_by_code'),
    path('employee-name/<str:pay_code>/', EmployeeNameByCodeAPIView.as_view(), name='employee-name'),


    path('attendance/import-excel/', ExcelUploadView.as_view(), name='import-excel'),
    
    path('upload-from-path/', ExcelUploadFromPathView.as_view(), name='upload-from-path'),


 

    path('employees-with-active-skills/', AllEmployeesWithActiveSkillsView.as_view(), name='employees-with-active-skills'),#http://172.50.4.138:8000/employees-with-active-skills/?name=ANKUR


    path('scheduled-employees-skills/', GroupedEmployeeSkillsView.as_view(), name='employees-skills-by-status'),

    path('employees-with-completed-skills/', AllEmployeesWithCompletedSkillsView.as_view(), name='employees-with-completed-skills'),

    path('multiskilling/reschedule/', create_rescheduled_multiskilling), #post

    path('multiskilling/rescheduled/', AllEmployeesWithRescheduledSkillsView.as_view(), name='rescheduled-skills'),#list

    path('subtopic/<int:subtopic_id>/', MCQBySubtopicView.as_view(), name='mcqs-by-subtopic'),


    path('training-summary/', TrainingSummaryView.as_view()),
    path('operators-joined-vs-trained/', OperatorsJoinedVsTrainedView.as_view()),
    path('msil-defects/', MSILDefectsView.as_view()),
    path('ctq-defects-all-plants/', CTQDefectsAllPlantsView.as_view()),
    path('internal-rejection/', InternalRejectionView.as_view()),
    path('upload-employee-excel/', EmployeeExcelUploadView.as_view(), name='upload-employee-excel'),


   # key event

    path('api/key-events/create/', views.KeyEventCreateView.as_view()),
    path('api/key-events/latest/', views.LatestKeyEventView.as_view()),
    path('api/connect-events/create/', views.connect_event_create, name='connect_event_create'),
    path('api/vote-events/create/', views.vote_event_create, name='vote_event_create'),
    path('api/question-papers/', views.QuestionPaperListCreateView.as_view()),
    path('api/questions/by-paper/<int:paper_id>/', views.QuestionsByPaperView.as_view()),
    path('api/questions/', views.QuestionListCreateView.as_view()),
    path('api/questions/<int:pk>/', views.QuestionDetailView.as_view()),

  

    path('api/employees/', views.EmployeeListCreateView.as_view(), name='employee_list_create'),

    path('api/start-test/', views.StartTestSessionView.as_view(), name='start_test_session'),
    path('api/end-test/', views.EndTestSessionView.as_view(), name='end_test_session'),
    path('api/scores/', views.ScoreListView.as_view(), name='score_list'),
    path('api/test-session/map/', views.KeyIdToEmployeeNameMap.as_view(), name='keyid-name-map'),
    path('api/past-sessions/', views.PastTestSessionsView.as_view()),
    path('api/scores-by-session/<str:name>/', views.ScoresByTestView.as_view()),
    path('api/score-summary/', views.ResultSummaryAPIView.as_view(), name='score-summary'),
    path('api/skills/', views.SkillListView.as_view(), name='skill-list'),
    path('api/scores-by-session/<path:name>/', views.ScoresByTestView.as_view()),


    



    #Employee Card 
    path('operator-skills-by-name/', OperatorSkillByNameView.as_view(), name='operator-skill-by-name'),
    path('scores-by-name/', ScoreByEmployeeNameView.as_view(), name='score-by-name'),
    path('multi-skilling-by-name/', MultiSkillingByEmployeeView.as_view(), name='multi-skilling-by-name'),
    path('refreshment-training-by-name/', RefreshmentTrainingByNameView.as_view(), name='refreshment-training-by-name'),
    path('employee-detail-by-name/', CardEmployeeDetailByNameView.as_view(), name='employee-detail-by-name'),



    path('employee-card-details/', EmployeeCardDetailsView.as_view(), name='employee-card-details'),


    path('employee-report/', EmployeeReportPDFView.as_view(), name='employee-report'),


    path('api/departments/', MainDepartmentListView.as_view(), name='department-list'),
    path('mainlines/<int:department_id>/', MainLinesByDepartmentView.as_view(), name='mainlines-by-department'),
    path('sublines/<int:main_line_id>/', SubLinesByMainLineView.as_view(), name='sublines-by-mainline'),
    path('stations/<int:sub_line_id>/', StationsBySubLineView.as_view(), name='stations-by-subline'),


    path('current-month/training-data/', CurrentMonthTrainingDataView.as_view(), name='current-month-training-data'),
    path('current-month/defects-data/', CurrentMonthDefectsDataView.as_view(), name='current-month-defects-data'),
    path('chart/operators/', OperatorsChartView.as_view(), name='operators-chart'),
    path('chart/training-plans/', TrainingPlansChartView.as_view(), name='training-plans-chart'),
    path('chart/defects-msil/', DefectsChartView.as_view(), name='defects-msil-chart'),


    path('upload-management-review/', ManagementReviewUploadView.as_view(), name='upload-management-review'),

    path('sublines/', views.SubLineListAPIView.as_view(), name='subline-list'),



    path('stations/<int:pk>/delete/', StationDeleteView.as_view(), name='station-delete'),
    path('stations/<int:pk>/update/', StationUpdateView.as_view(), name='station-update'),


    path('departments-by-factory/', DepartmentByFactoryView.as_view(), name='departments-by-factory'),
    path('manpower-ctq-trends/', ManpowerCTQTrendsView.as_view(), name='manpower-ctq-trends'),
    path('upload-ctq/', UploadAdvancedManpowerCTQView.as_view(), name='upload_ctq'),

   
    path('api/logo/', LogoView.as_view()),



    path('download-all/', UploadedFileListView.as_view(), name='download_all_files'),
    path('download-file/<int:file_id>/', FileDownloadView.as_view(), name='download_file'),



    path('employees/level-one/', LevelOneEmployeesView.as_view(), name='level-one-employees'),
    path('grouped-scores/', GroupedScoreByEmployeeView.as_view(), name='grouped-scores'),
    path('grouped-scores-level-three/', GroupedLevelThreeScoreByEmployeeView.as_view(), name='grouped-scores-level-three'),



    # path('set-task-time/', SetTaskTimeView.as_view(), name='set-task-time'),


    path('set-task-time/attendance/', SetAttendanceTaskTimeView.as_view()),
    path('set-task-time/management-review/', SetManagementReviewTaskTimeView.as_view()),
    path('set-task-time/advanced-manpower/', SetAdvancedManpowerTaskTimeView.as_view()),
    path('upload-operator-skills/', UploadOperatorSkillsAPIView.as_view(), name='upload_operator_skills_matrix'),

    # level 0
    path('temp-user-info/', UserInfoListCreateView.as_view(), name='create_user_info'),
    path('human-body-checks/', HumanBodyCheckListCreateView.as_view(), name='human-body-check-create'),
    path('human-body-checks/list/', HumanBodyCheckListCreateView.as_view(), name='human-body-check-list'),

    path('passed-users/', PassedUsersWithDetailsView.as_view(), name='passed-users'),
    path('allpassed-users/', AllPassedUsersView.as_view(), name='all_passed_users'),
    path('user-body-checks/', UserInfoBodyCheckListView.as_view(), name='user_body_check_list'),
    path('remaining-departments/', RemainingDepartmentsView.as_view(), name='remaining-departments'),
    path('users/<str:temp_id>/', UserInfoUpdateView.as_view(), name='user-update'),
    path('training-batches/active/', ActiveTrainingBatchListView.as_view(), name='active-training-batches'),
    path('training-batches/past/', PastTrainingBatchListView.as_view(), name='past-training-batches'),
    path('attendance-detail/<str:batch_id>/', BatchAttendanceDetailView.as_view(), name='batch-attendance-detail'),
    path('attendances/', BulkAttendanceUpdateView.as_view(), name='bulk-attendance-update'),
    path('batches/<str:batch_id>/complete/', CompleteTrainingBatchView.as_view(), name='complete-training-batch'),


    path('submit-web-test/', SubmitWebTestAPIView.as_view(), name='submit-web-test'),



    
    # path('materials/<int:pk>/serve/', serve_material_file, name='serve-material-file'),
    path('han-materials/<int:pk>/serve/', serve_han_material_file, name='serve-han-material-file'),

    # URL for Shokuchou files
    path('sho-materials/<int:pk>/serve/', serve_sho_material_file, name='serve-sho-material-file'),

    path('operator-skills/<int:pk>/download-certificate/', OperatorSkillCertificatePDF.as_view(), name='download-skill-certificate'),
    path('hanchou-results/<int:pk>/download-certificate/', HanchouResultCertificatePDF.as_view(), name='download-hanchou-certificate'),
    path('shokuchou-results/<int:pk>/download-certificate/', ShokuchouResultCertificatePDF.as_view(), name='download-shokuchou-certificate'),
    path('scores/<int:pk>/download-certificate/', ScoreCertificatePDF.as_view(), name='score-download-certificate'),




    path('skill-matrix-excel/', SkillMatrixExcelView.as_view(), name='skill_matrix_excel'),




    path('ojt-report-pdf/', LevelTwoOJTReportPDFView.as_view(), name='ojt_report_pdf'),
    path('ojt-report/quality/', LevelTwoQAReportPDFView.as_view(), name='ojt_report_quality'),
    path('level-three-ojt-report-pdf/', LevelThreeOJTReportPDFView.as_view(), name='level_three_ojt_report_pdf'), 




    path('get-plan-data/', get_plan_data, name='get_plan_data'),
    path('get-plan-totals/', get_plan_totals, name='get_plan_totals'),
    path('get-plan-other/', get_plan_other, name='get_plan_other'),



    path('level3-qa-report-pdf/', LevelThreeQAReportPDFView.as_view(), name='level3_qa_report_pdf'),




    path('current-month/training-data/', CurrentMonthTrainingDataView.as_view(), name='current-month-training-data'),
    path('current-month/defects-data/', CurrentMonthDefectsDataView.as_view(), name='current-month-defects-data'),
    path('previous-month/defects-data/', views.PreviousMonthDefectsDataView.as_view(), name='previous-month-defects-data'),
    path('next-month/defects-data/', views.NextMonthDefectsDataView.as_view(), name='next-month-defects-data'),


    path('api/notifications/count/', notification_count, name='notification-count'),
    path('api/notifications/system/', create_system_notification, name='create-system-notification'),
    path('api/notifications/test/', create_test_notification, name='create-test-notification'),
    path('api/notifications/debug/', test_notifications, name='test-notifications'),
    path('api/notifications/trigger-employee/', trigger_employee_notification, name='trigger-employee-notification'),
    path('api/notifications/trigger-all-types/', trigger_all_notification_types, name='trigger-all-notification-types'),
    path('api/notifications/delete_all/', delete_all_notifications, name='delete-all-notifications'),

    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

