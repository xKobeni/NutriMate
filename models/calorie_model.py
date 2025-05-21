class CalorieCalculator:
    # Activity level multipliers
    ACTIVITY_MULTIPLIERS = {
        'sedentary': 1.2,      # Little or no exercise
        'light': 1.375,        # Light exercise 1-3 days/week
        'moderate': 1.55,      # Moderate exercise 3-5 days/week
        'very': 1.725,         # Hard exercise 6-7 days/week
        'extra': 1.9           # Very hard exercise & physical job
    }

    @staticmethod
    def calculate_bmr(weight, height, age, gender):
        """
        Calculate Basal Metabolic Rate (BMR) using the Harris-Benedict equation
        weight in kg, height in cm, age in years
        """
        if gender == 'male':
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:  # female
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        return round(bmr)

    @staticmethod
    def calculate_tdee(bmr, activity_level):
        """
        Calculate Total Daily Energy Expenditure (TDEE)
        """
        multiplier = CalorieCalculator.ACTIVITY_MULTIPLIERS.get(activity_level, 1.2)
        return round(bmr * multiplier)

    @staticmethod
    def calculate_calorie_needs(weight, height, age, gender, activity_level, goal='maintain'):
        """
        Calculate daily calorie needs based on user's profile and goal
        Returns a dictionary with various calorie targets
        """
        bmr = CalorieCalculator.calculate_bmr(weight, height, age, gender)
        tdee = CalorieCalculator.calculate_tdee(bmr, activity_level)

        # Calculate calorie targets based on goals
        calorie_targets = {
            'maintain': tdee,
            'lose': round(tdee - 500),  # 500 calorie deficit for weight loss
            'gain': round(tdee + 500)   # 500 calorie surplus for weight gain
        }

        # Calculate macronutrient distribution
        macros = {
            'maintain': {
                'protein': round(weight * 1.6),  # 1.6g per kg of body weight
                'carbs': round((tdee * 0.45) / 4),  # 45% of calories from carbs
                'fat': round((tdee * 0.35) / 9)     # 35% of calories from fat
            },
            'lose': {
                'protein': round(weight * 2.0),  # 2.0g per kg of body weight
                'carbs': round((calorie_targets['lose'] * 0.40) / 4),  # 40% of calories from carbs
                'fat': round((calorie_targets['lose'] * 0.30) / 9)     # 30% of calories from fat
            },
            'gain': {
                'protein': round(weight * 1.8),  # 1.8g per kg of body weight
                'carbs': round((calorie_targets['gain'] * 0.50) / 4),  # 50% of calories from carbs
                'fat': round((calorie_targets['gain'] * 0.30) / 9)     # 30% of calories from fat
            }
        }

        return {
            'bmr': bmr,
            'tdee': tdee,
            'calorie_targets': calorie_targets,
            'macros': macros,
            'recommendations': {
                'maintain': {
                    'calories': calorie_targets['maintain'],
                    'protein': macros['maintain']['protein'],
                    'carbs': macros['maintain']['carbs'],
                    'fat': macros['maintain']['fat']
                },
                'lose': {
                    'calories': calorie_targets['lose'],
                    'protein': macros['lose']['protein'],
                    'carbs': macros['lose']['carbs'],
                    'fat': macros['lose']['fat']
                },
                'gain': {
                    'calories': calorie_targets['gain'],
                    'protein': macros['gain']['protein'],
                    'carbs': macros['gain']['carbs'],
                    'fat': macros['gain']['fat']
                }
            }
        } 