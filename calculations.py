# constants
baseline_temp = 60
mass_gal_wat = 3.785
c_wat = 4184
joules_per_kwh = 3.6E6
gal_per_min = 2.1
water_treatment_kwh_per_mg = 1200
lbs_per_kwh = 0.96
electric_rate = 0.10

with open("anonymized_data.csv", "r") as file:
    raw_users = file.read().splitlines()[1:]


def fahrenheit_to_celcius(n):
    return (n - 32) * (5/9)


def convert_temp(s):
    if s == "Cold":
        return 60
    elif s == "Lukewarm":
        return 100
    elif s == "Warm":
        return 105
    elif s == "Super Hot":
        return 110
    else:
        return 1


class Reducer:
    def __init__(self, reduction_length, challenge_duration, temperature):
        self.reduction_length = reduction_length
        self.challenge_duration = challenge_duration
        self.temperature = temperature
        self.carbon_savings = self.calculate_carbon_savings()
        self.cost_savings = self.calculate_cost_savings()

    def calculate_carbon_savings(self):
        change_temp = fahrenheit_to_celcius(
            self.temperature) - fahrenheit_to_celcius(baseline_temp)
        energy_heat_per_gal = mass_gal_wat * c_wat * change_temp
        self.kwh_min_heat = (energy_heat_per_gal /
                             joules_per_kwh) * gal_per_min
        kwh_min_treat = (water_treatment_kwh_per_mg / 1E6) * gal_per_min
        kwh_min_total = self.kwh_min_heat + kwh_min_treat
        emissions_min = kwh_min_total * lbs_per_kwh
        emissions_total = emissions_min * \
            self.reduction_length * 30 * self.challenge_duration
        return emissions_total

    def calculate_cost_savings(self):
        cost_min = electric_rate * self.kwh_min_heat
        cost_year = cost_min * reduction_length * 365
        return cost_year


users = []

# iterate for each user and scrape important data
for user in raw_users:
    user_string = user.split(",")
    print(user_string)
    if user_string[2] == "No":
        continue

    reduction_length = int(user_string[3].strip('"')[0])
    challenge_duration = 12
    if (user_string[4].strip('"')[0] == "6"):
        challenge_duration = 6
    print(challenge_duration)
    temperature = convert_temp(user_string[6].strip('"'))
    users.append(
        Reducer(reduction_length, challenge_duration, temperature)
    )

total_carbon_savings = 0
total_cost_savings = 0

for user in users:
    total_carbon_savings += user.carbon_savings
    total_cost_savings += user.cost_savings


print(total_carbon_savings)
print(total_cost_savings / len(users))
