import skfuzzy as fuzzy
import numpy as np 
from skfuzzy import control as ctrl
import random

times = ['breakfast', 'lunch', 'dinner', 'snack']
styles = ['mediterranean', 'mexican', 'cuban', 'asian']

class RecipeRecommendationSystem:
    def __init__(self):
        self.diabetes = ctrl.Antecedent(np.arange(0,11,1), 'diabetes')
        self.heart_disease = ctrl.Antecedent(np.arange(0,11,1), 'heart_disease')
        self.cold = ctrl.Antecedent(np.arange(0, 11, 1), 'cold')
        self.recommended_dish = ctrl.Consequent(np.arange(0, 18, 1), 'recommended_dish')
        self._create_universes()
        self._create_membership_functions()
        self._create_rules()

    

    def _create_universes(self):
        self.diabetes.automf(3)
        self.heart_disease.automf(3)
        self.cold.automf(3)

        # Define el universo de salida como una lista de platillos específicos
        self.recommended_dish['low_sugar_and_low_salt_and_C'] = fuzzy.trimf(self.recommended_dish.universe, [0, 2, 3])
        self.recommended_dish['low_salt_and_C'] = fuzzy.trimf(self.recommended_dish.universe, [2, 4, 5])
        self.recommended_dish['low_sugar_and_C'] = fuzzy.trimf(self.recommended_dish.universe, [4, 6, 7])
        self.recommended_dish['low_sugar_and_low_salt'] = fuzzy.trimf(self.recommended_dish.universe, [6, 8, 9])
        self.recommended_dish['low_salt'] = fuzzy.trimf(self.recommended_dish.universe, [8, 10, 11])   
        self.recommended_dish['low_sugar'] = fuzzy.trimf(self.recommended_dish.universe, [10, 12, 13])
        self.recommended_dish['with_C'] = fuzzy.trimf(self.recommended_dish.universe, [12, 14, 15])
        self.recommended_dish['normal'] = fuzzy.trimf(self.recommended_dish.universe, [14, 16, 17])
        

    def _create_membership_functions(self):
        self.heart_disease['low'] = fuzzy.trimf(self.heart_disease.universe, [0, 2, 4])
        self.heart_disease['average'] = fuzzy.trimf(self.heart_disease.universe, [3, 5, 7])
        self.heart_disease['high'] = fuzzy.trimf(self.heart_disease.universe, [6, 8, 10])
        self.diabetes['low'] = fuzzy.trimf(self.diabetes.universe, [0, 2, 4])
        self.diabetes['average'] = fuzzy.trimf(self.diabetes.universe, [3, 5, 7])
        self.diabetes['high'] = fuzzy.trimf(self.diabetes.universe, [6, 8, 10])
        self.cold['low'] = fuzzy.trimf(self.diabetes.universe, [0, 2, 4])
        self.cold['average'] = fuzzy.trimf(self.diabetes.universe, [3, 5, 7])
        self.cold['high'] = fuzzy.trimf(self.diabetes.universe, [6, 8, 10])

    def _create_rules(self):
        rule1 = ctrl.Rule((self.diabetes['high'] | self.diabetes['average']) & (self.heart_disease['high'] | self.heart_disease['average']) & (self.cold['high'] | self.cold['average']), self.recommended_dish['low_sugar_and_low_salt_and_C'])
        rule2 = ctrl.Rule((self.diabetes['high'] | self.diabetes['average']) & self.heart_disease['low'] & self.cold['low'], self.recommended_dish['low_sugar'])
        rule3 = ctrl.Rule(self.diabetes['low'] & (self.heart_disease['high'] | self.heart_disease['average']) & self.cold['low'], self.recommended_dish['low_salt'])
        rule4 = ctrl.Rule(self.diabetes['low'] & self.heart_disease['low'] & (self.cold['high'] | self.cold['average']), self.recommended_dish['with_C'])
        rule5 = ctrl.Rule((self.diabetes['high'] | self.diabetes['average']) & (self.heart_disease['high'] | self.heart_disease['average']) & self.cold['low'], self.recommended_dish['low_sugar_and_low_salt'])
        rule6 = ctrl.Rule(self.diabetes['low'] & self.heart_disease['low'] & self.cold['low'], self.recommended_dish['normal'])
        rule7 = ctrl.Rule(self.diabetes['low'] & (self.heart_disease['high'] | self.heart_disease['average']) & (self.cold['average'] | self.cold['high']), self.recommended_dish['low_salt_and_C'])
        rule8 = ctrl.Rule((self.diabetes['average'] | self.diabetes['high']) & self.heart_disease['low'] & (self.cold['average'] | self.cold['high']), self.recommended_dish['low_sugar_and_C'])
        
        self.recipe_recommendation_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8])
        self.recipe_recommendation = ctrl.ControlSystemSimulation(self.recipe_recommendation_ctrl)

    

    def recommend_recipe(self, diabetes, heart_disease, cold):
        self.recipe_recommendation.input['diabetes'] = diabetes
        self.recipe_recommendation.input['heart_disease'] = heart_disease
        self.recipe_recommendation.input['cold'] = cold
        self.recipe_recommendation.compute()
        out = self.recipe_recommendation.output['recommended_dish']
        # Mapea el valor de salida a un platillo específico
        recommended_dish = self._map_to_dish(self.recipe_recommendation.output['recommended_dish'])
        return recommended_dish

    def _map_to_dish(self, output_value):
        # Define una función de mapeo de salida difusa a platillo específico
        if output_value < 3:
            return "Muy sano, bajo de sal y azucar y rico en vitamina C"
        elif output_value < 5:
            return "Muy sano, bajo de sal y rico en vitamina C"
        elif output_value < 7:
            return "Muy sano, bajo de azúcar y rico en vitamina C"
        elif output_value < 9:
            return "Muy sano, bajo de sal y azúcar"
        elif output_value < 11:
            return "Bajo de sal"
        elif output_value < 13:
            return "Bajo de azúcar"
        elif output_value < 15:
            return "Rico en vitamina C"
        else: return "Normal"


    def __call__(self, *args: np.Any, **kwds: np.Any):
         return self.recommend_recipe(args)
    



class CulinaryStyleRecommendation:
    def __init__(self):
            self.cuban = ctrl.Antecedent(np.arange(0,11,1), 'cuban')
            self.mediterranean = ctrl.Antecedent(np.arange(0,11,1), 'mediterranean')
            self.mexican = ctrl.Antecedent(np.arange(0,11,1), 'mexican')
            self.asian = ctrl.Antecedent(np.arange(0,11,1), 'asian')
            
            self.current_hour = ctrl.Antecedent(np.arange(0, 24, 1), 'current_hour')

            self.culinary_style = ctrl.Consequent(np.arange(0,34,1), 'culinary_style')
            
            self._create_universes()
            self._create_rules()

    def _create_universes(self):
        self.cuban.automf(3)
        self.mediterranean.automf(3)
        self.mexican.automf(3)
        self.asian.automf(3)

        self.current_hour['snack'] = fuzzy.trimf(self.current_hour.universe, [0, 1, 5])
        self.current_hour['breakfast'] = fuzzy.trimf(self.current_hour.universe, [4, 11, 12])
        self.current_hour['lunch'] = fuzzy.trimf(self.current_hour.universe, [11, 14, 17])
        self.current_hour['snack'] = fuzzy.trimf(self.current_hour.universe, [16, 18, 20])
        self.current_hour['dinner'] = fuzzy.trimf(self.current_hour.universe, [16, 20, 23])
        self.current_hour['snack'] = fuzzy.trimf(self.current_hour.universe, [22, 23, 24])

        self.culinary_style['mediterranean_breakfast'] = fuzzy.trimf(self.culinary_style.universe, [0, 2, 3])
        self.culinary_style['mexican_breakfast'] = fuzzy.trimf(self.culinary_style.universe, [2, 4, 5])
        self.culinary_style['cuban_breakfast'] = fuzzy.trimf(self.culinary_style.universe, [4, 6, 7])
        self.culinary_style['asian_breakfast'] = fuzzy.trimf(self.culinary_style.universe, [6, 8, 9])
        
        self.culinary_style['mediterranean_lunch'] = fuzzy.trimf(self.culinary_style.universe, [8, 10, 11])
        self.culinary_style['mexican_lunch'] = fuzzy.trimf(self.culinary_style.universe, [10, 12, 13])
        self.culinary_style['cuban_lunch'] = fuzzy.trimf(self.culinary_style.universe, [12, 14, 15])
        self.culinary_style['asian_lunch'] = fuzzy.trimf(self.culinary_style.universe, [14, 16, 17])
        
        self.culinary_style['mediterranean_dinner'] = fuzzy.trimf(self.culinary_style.universe, [16, 18, 19])
        self.culinary_style['mexican_dinner'] = fuzzy.trimf(self.culinary_style.universe, [18, 20, 21])
        self.culinary_style['cuban_dinner'] = fuzzy.trimf(self.culinary_style.universe, [20, 22, 23])
        self.culinary_style['asian_dinner'] = fuzzy.trimf(self.culinary_style.universe, [22, 24, 25])
        
        self.culinary_style['mediterranean_snack'] = fuzzy.trimf(self.culinary_style.universe, [24, 26, 27])
        self.culinary_style['mexican_snack'] = fuzzy.trimf(self.culinary_style.universe, [26, 28, 29])
        self.culinary_style['cuban_snack'] = fuzzy.trimf(self.culinary_style.universe, [28, 30, 31])
        self.culinary_style['asian_snack'] = fuzzy.trimf(self.culinary_style.universe, [30, 32, 33])

        self.mediterranean['low'] = fuzzy.trimf(self.mediterranean.universe, [0,2,4])
        self.mediterranean['average'] = fuzzy.trimf(self.mediterranean.universe, [3, 5, 7])
        self.mediterranean['high'] = fuzzy.trimf(self.mediterranean.universe, [6, 8, 10])

        self.cuban['low'] = fuzzy.trimf(self.cuban.universe, [0, 2, 4])
        self.cuban['average'] = fuzzy.trimf(self.cuban.universe, [3, 5, 7])
        self.cuban['high'] = fuzzy.trimf(self.cuban.universe, [6, 8, 10])

        self.mexican['low'] = fuzzy.trimf(self.mexican.universe, [0, 2, 4])
        self.mexican['average'] = fuzzy.trimf(self.mexican.universe, [3, 5, 7])
        self.mexican['high'] = fuzzy.trimf(self.mexican.universe, [6, 8, 10])

        self.asian['low'] = fuzzy.trimf(self.asian.universe, [0, 2, 4])
        self.asian['average'] = fuzzy.trimf(self.asian.universe, [3, 5, 7])
        self.asian['high'] = fuzzy.trimf(self.asian.universe, [6, 8, 10])


    
        
    def _create_rules(self):
            rules = []
            random_style = random.randint(0, len(styles)-1)

            for i in times:
                rule1 = ctrl.Rule(self.cuban['low'] & self.mexican['low'] & self.mediterranean['low'] & self.asian['low'] & self.current_hour[i], self.culinary_style[styles[random_style]+'_'+i])
                rule2 = ctrl.Rule(self.cuban['average'] & self.mexican['average'] & self.mediterranean['average'] & self.asian['average'] & self.current_hour[i], self.culinary_style[styles[random_style]+'_'+i])
                rule3 = ctrl.Rule(self.cuban['high'] & self.mexican['high'] & self.mediterranean['high'] & self.asian['high'] & self.current_hour[i], self.culinary_style[styles[random_style]+'_'+i])
                rules += [rule1,rule2, rule3]
                rule1 = ctrl.Rule(self.cuban['high'] & (self.mexican['low'] | self.mexican['average']) & (self.mediterranean['low'] | self.mediterranean['average']) & (self.asian['low'] | self.asian['average']) & self.current_hour[i], self.culinary_style['cuban_'+i])
                rule2 = ctrl.Rule((self.cuban['low'] | self.cuban['average']) & self.mexican['high'] & (self.mediterranean['low'] | self.mediterranean['average']) & (self.asian['low'] | self.asian['average']) & self.current_hour[i], self.culinary_style['mexican_'+i])
                rule3 = ctrl.Rule((self.cuban['low'] | self.cuban['average']) & (self.mexican['low'] | self.mexican['average']) & self.mediterranean['high'] & (self.asian['low'] | self.asian['average']) & self.current_hour[i], self.culinary_style['mediterranean_'+i])
                rule4 = ctrl.Rule((self.cuban['low'] | self.cuban['average']) & (self.mexican['low'] | self.mexican['average']) & (self.mediterranean['low'] | self.mediterranean['average']) & self.asian['high'] & self.current_hour[i], self.culinary_style['asian_'+i])
                rules += [rule1,rule2,rule3,rule4]
            for i in times:
                rule1 = ctrl.Rule(self.cuban['average'] & self.mexican['low'] & self.mediterranean['low'] & self.asian['low'] & self.current_hour[i], self.culinary_style['cuban_'+i])
                rule2 = ctrl.Rule(self.cuban['low'] & self.mexican['average'] & self.mediterranean['low'] & self.asian['low'] & self.current_hour[i], self.culinary_style['mexican_'+i])
                rule3 = ctrl.Rule(self.cuban['low'] & self.mexican['low'] & self.mediterranean['average'] & self.asian['low'] & self.current_hour[i], self.culinary_style['mediterranean_'+i])
                rule4 = ctrl.Rule(self.cuban['low'] & self.mexican['low'] & self.mediterranean['low'] & self.asian['average'] & self.current_hour[i], self.culinary_style['asian_'+i])
                rules += [rule1,rule2,rule3,rule4]

            for i in times:
                rule1 = ctrl.Rule(self.cuban['average'] & (self.mexican['low'] | self.mexican['average']) & (self.mediterranean['low'] | self.mediterranean['average']) & (self.asian['low'] | self.asian['average']) & self.current_hour[i], self.culinary_style['cuban_'+i])
                rule2 = ctrl.Rule((self.cuban['low'] | self.cuban['average']) & self.mexican['average'] & (self.mediterranean['low'] | self.mediterranean['average']) & (self.asian['low'] | self.asian['average']) & self.current_hour[i], self.culinary_style['mexican_'+i])
                rule3 = ctrl.Rule((self.cuban['low'] | self.cuban['average']) & (self.mexican['low'] | self.mexican['average']) & self.mediterranean['average'] & (self.asian['low'] | self.asian['average']) & self.current_hour[i], self.culinary_style['mediterranean_'+i])
                rule4 = ctrl.Rule((self.cuban['low'] | self.cuban['average']) & (self.mexican['low'] | self.mexican['average']) & (self.mediterranean['low'] | self.mediterranean['average']) & self.asian['average'] & self.current_hour[i], self.culinary_style['asian_'+i])
                rules += [rule1,rule2,rule3,rule4]

            self.culinary_style_recommendation_ctrl = ctrl.ControlSystem(rules)
            self.culinary_style_recommendation = ctrl.ControlSystemSimulation(self.culinary_style_recommendation_ctrl)

            pass
    

    def recommend_culinary_style(self, mediterranean, mexican, cuban, asian, current_hour):
        self.culinary_style_recommendation.input['cuban'] = cuban
        self.culinary_style_recommendation.input['mediterranean'] = mediterranean
        self.culinary_style_recommendation.input['mexican'] = mexican
        self.culinary_style_recommendation.input['asian'] = asian
        
        self.culinary_style_recommendation.input['current_hour'] = current_hour
        
        self.culinary_style_recommendation.compute()
        self.culinary_style_recommendation.output['culinary_style']
        recommend_style = self._map_to_style(self.culinary_style_recommendation.output['culinary_style'])
        return recommend_style


    def _map_to_style(self, value):
        if value < 3:
            return 'Desayuno mediterraneo'
        elif value<5:
             return 'Desayuno mexicano'
        elif value <7:
             return 'Desayuno cubano'
        elif value <9:
             return 'Desayuno asiatico'
        elif value <11:
             return 'Almuerzo mediterraneo'
        elif value <13:
            return 'Almuerzo mexicano'
        elif value <15:
            return 'Almuero cubano'
        elif value <17:
            return 'Almuerzo asiatico'
        elif value <19:
            return 'Cena mediterranea'
        elif value <21:
            return 'Cena mexicana'
        elif value <23:
            return 'Cena cubana'
        elif value <25:
            return 'Cena asiatica'
        elif value <27:
            return 'Merienda mediterranea'
        elif value <29:
            return 'Merienda mexicana'
        elif value <31:
            return 'Merienda cubana'
        elif value <33:
            return 'Merienda asiatica'
        
    def __call__(self, *args: np.Any, **kwds: np.Any):
        return self.recommend_culinary_style(args)


def call_recommenders(diseases,culinary_styles, hour):
    mediterranean = culinary_styles['mediterranean']
    mexican = culinary_styles['mexican']
    cuban = culinary_styles['cuban']
    asian = culinary_styles['asian']

    diabetes = diseases['diabetes']
    heart_disease = diseases['heart_disease']

    culinary_style_recommender = CulinaryStyleRecommendation()
    culinary_style: str = culinary_style_recommender.recommend_culinary_style(mediterranean, mexican, cuban, asian, hour)
    recipe_recommender = RecipeRecommendationSystem()
    culinary_constraint: str = recipe_recommender.recommend_recipe(diabetes, heart_disease)
    return culinary_style.lower() + culinary_constraint.lower()

# Ejemplo de uso
# if __name__ == "__main__":
#     system = RecipeRecommendationSystem()
#     # Ejemplo de gustos y condiciones médicas del usuario
#     diabetes = 3
#     heart_disease = 1  # Por ejemplo, tiene una condición médica moderada
#     recommended_dish = system.recommend_recipe(diabetes, heart_disease)
#     print("Recommended dish based on taste and health condition:", recommended_dish)

