from django.core.mail import send_mail
from django.conf import settings

def send_milestone_email(subject, message, recipient_list):
    """
    Sends a plain text email to multiple recipients.
    """
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
    )














# utils.py

from .models import LevelTwoTraineeInfo, Score, OperatorSkill,EmployeeMaster
from django.db import transaction

def check_and_update_operator_skill(trainee_id):
    try:
        # Get the trainee info
        trainee = LevelTwoTraineeInfo.objects.get(traineeId=trainee_id)

        # 🛠 Match based on pay_code instead of emp_id
        employee = EmployeeMaster.objects.get(pay_code=trainee_id)

        # Calculate and update training status
        training_status = trainee.calculate_and_save_training_status()

        # Check for the latest score
        latest_score = Score.objects.filter(employee=employee).order_by('-created_at').first()

        if training_status == "Pass" and latest_score and latest_score.passed:
            station = latest_score.skill
            level = latest_score.level

            if not station or not level:
                print("Station or level not provided in score.")
                return False

            with transaction.atomic():
                skill_obj, created = OperatorSkill.objects.update_or_create(
                    operator=employee,
                    station=station,
                    defaults={'skill_level': level}
                )
                print(f"OperatorSkill {'created' if created else 'updated'} for {employee.name}")
                return True

        else:
            print("Training or test not passed.")
            return False

    except LevelTwoTraineeInfo.DoesNotExist:
        print(f"Trainee with ID {trainee_id} does not exist.")
        return False

    except EmployeeMaster.DoesNotExist:
        print(f"Employee with pay_code {trainee_id} does not exist.")
        return False

    except Exception as e:
        print(f"Error: {str(e)}")
        return False







from .models import LevelThreeTraineeInfo, Score, OperatorSkill, EmployeeMaster
from django.db import transaction

def check_and_update_operator_skill_level_three(trainee_id):
    try:
        # Get trainee
        trainee = LevelThreeTraineeInfo.objects.get(trainee_Id=trainee_id)

        # Get employee based on pay_code = trainee_id
        employee = EmployeeMaster.objects.get(pay_code=trainee_id)

        # Recalculate training status
        training_status = trainee.calculate_and_save_training_status()

        # Get latest test score for this employee
        latest_score = Score.objects.filter(employee=employee).order_by('-created_at').first()

        if training_status == "Pass" and latest_score and latest_score.passed:
            station = latest_score.skill
            level = latest_score.level

            if not station or not level:
                print("Missing station or level in latest score.")
                return False

            with transaction.atomic():
                
                skill_obj, created = OperatorSkill.objects.update_or_create(
                    operator=employee,
                    station=station,
                    defaults={'skill_level': level}
                )
                print(f"OperatorSkill {'created' if created else 'updated'} for {employee.name}")
                return True

        else:
            print("Either training or test not passed.")
            return False

    except LevelThreeTraineeInfo.DoesNotExist:
        print(f"No Level 3 trainee found for ID {trainee_id}")
        return False

    except EmployeeMaster.DoesNotExist:
        print(f"No Employee found with pay_code {trainee_id}")
        return False

    except Exception as e:
        print(f"Error during Level 3 skill update: {str(e)}")
        return False

