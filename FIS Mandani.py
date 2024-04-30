import warnings
warnings.filterwarnings('ignore')
import numpy as np
import skfuzzy as fuzz # Generar MFs
from skfuzzy import control as ctrl # inferencia

# Antecedentes
quality = ctrl.Antecedent(np.arange(0, 11, 1), 'quality')
service = ctrl.Antecedent(np.arange(0, 11, 1), 'service')

# Consequent
tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip')

# genera automaticamente 3 MFs para cada antecedente
quality.automf(3)
service.automf(3)

# Customised Triangular MFs, 0 - 25
tip['low'] = fuzz.trimf(tip.universe, [0, 0, 12])
tip['medium'] = fuzz.trimf(tip.universe, [5, 13, 20])
tip['high'] = fuzz.trimf(tip.universe, [15, 25, 25])
# Visualización de antecedentes
quality.view()
tip['medium'].view()