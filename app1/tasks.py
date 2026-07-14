# import os
# from celery import shared_task
# from tablib import Dataset
# from .resources import BiometricAttendanceResource

# @shared_task
# def import_attendance_from_excel():
#     EXCEL_FILE_PATH = r"E:\attendance.xlsx"

#     if not os.path.exists(EXCEL_FILE_PATH):
#         return {'status': 'failed', 'reason': 'Excel file not found'}

#     file_format = 'xls' if EXCEL_FILE_PATH.endswith('.xls') else 'xlsx'
#     dataset = Dataset()

#     try:
#         with open(EXCEL_FILE_PATH, 'rb') as file_obj:
#             imported_data = dataset.load(file_obj.read(), format=file_format)
#     except Exception as e:
#         return {'status': 'failed', 'reason': f'File read error: {str(e)}'}

#     resource = BiometricAttendanceResource()
#     result = resource.import_data(imported_data, dry_run=True)

#     if result.has_errors():
#         errors = []
#         for row_number, row_errors in result.row_errors():
#             for error in row_errors:
#                 errors.append(f"Row {row_number}: {str(error.error)}")
#         return {'status': 'failed', 'errors': errors}

#     resource.import_data(imported_data, dry_run=False)
#     return {'status': 'success', 'message': 'Data imported successfully'}








import os
import pandas as pd
from celery import shared_task
from tablib import Dataset
from .resources import BiometricAttendanceResource
from .models import ManagementReview, AdvancedManpowerCTQ, Factory, Department, HQ

@shared_task
def import_attendance_from_excel():
    EXCEL_FILE_PATH = r"D:\Datashare\attendance.xlsx"

    if not os.path.exists(EXCEL_FILE_PATH):
        return {'status': 'failed', 'reason': 'Excel file not found'}

    dataset = Dataset()
    try:
        with open(EXCEL_FILE_PATH, 'rb') as f:
            dataset.load(f.read(), format='xlsx')
    except Exception as e:
        return {'status': 'failed', 'reason': str(e)}

    resource = BiometricAttendanceResource()
    result = resource.import_data(dataset, dry_run=True)
    if result.has_errors():
        return {'status': 'failed', 'errors': str(result.row_errors())}

    resource.import_data(dataset, dry_run=False)
    return {'status': 'success', 'message': 'Attendance imported successfully'}

@shared_task
def import_management_review_from_excel():
    FILE = r"D:\Datashare\management_review.xlsx"
    if not os.path.exists(FILE):
        return {'status': 'failed', 'reason': 'File not found'}

    try:
        df = pd.read_excel(FILE, header=1)
        df.columns = df.columns.str.strip()
        for _, row in df.iterrows():
            ManagementReview.objects.update_or_create(
                month_year=pd.to_datetime(row['Month & Year']).date(),
                defaults={
                    'new_operators_joined': int(row['New Operators Joined']),
                    'new_operators_trained': int(row['New Operators Trained']),
                    'total_training_plans': int(row['Total Training Plans']),
                    'total_trainings_actual': int(row['Total Trainings Actual']),
                    'total_defects_msil': int(row['Total Defects at MSIL']),
                    'ctq_defects_msil': int(row['CTQ Defects at MSIL']),
                    'total_defects_tier1': int(row['Total Defects at Tier-1']),
                    'ctq_defects_tier1': int(row['CTQ Defects at Tier-1']),
                    'total_internal_rejection': int(row['Total Internal Rejection']),
                    'ctq_internal_rejection': int(row['CTQ Internal Rejection']),
                }
            )
        return {'status': 'success', 'message': 'Management review imported'}
    except Exception as e:
        return {'status': 'failed', 'error': str(e)}

@shared_task
def import_advanced_manpower_from_excel():
    FILE = r"D:\Datashare\advanced_manpower_ctq.xlsx"
    if not os.path.exists(FILE):
        return {'status': 'failed', 'reason': 'File not found'}

    try:
        df = pd.read_excel(FILE)
        for _, row in df.iterrows():
            hq, _ = HQ.objects.get_or_create(name='Default HQ')
            factory, _ = Factory.objects.get_or_create(name=row['factory_name'], defaults={'hq': hq})
            department, _ = Department.objects.get_or_create(name=row['department_name'], factory=factory)

            AdvancedManpowerCTQ.objects.create(
                month_year_ctq=row['month_year_ctq'],
                total_stations_ctq=row['total_stations_ctq'],
                operator_required_ctq=row['operator_required_ctq'],
                operator_availability_ctq=row['operator_availability_ctq'],
                buffer_manpower_required_ctq=row['buffer_manpower_required_ctq'],
                buffer_manpower_availability_ctq=row['buffer_manpower_availability_ctq'],
                attrition_trend_ctq=row['attrition_trend_ctq'],
                absentee_trend_ctq=row['absentee_trend_ctq'],
                planned_units_ctq=row['planned_units_ctq'],
                actual_production_ctq=row['actual_production_ctq'],
                factory=factory,
                department=department
            )
        return {'status': 'success', 'message': 'Advanced manpower imported'}
    except Exception as e:
        return {'status': 'failed', 'error': str(e)}
