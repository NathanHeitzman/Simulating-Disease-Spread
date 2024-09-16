import random

def infect(infect_rate:float) -> bool:
    """Takes a float (infect_rate) which acts as the probability of
    infection, and returns a boolean value of True or False to represent
    if a person is infected"""
    infect_num = random.uniform(0,1)
    if infect_num < infect_rate:
        return True
    else:
        return False

def recover(recovery_rate:float) -> bool:
    """Takes a float (recovery_rate) which acts as the probability of
    an infected individual recovering, and returns a boolean value of
    True or False to represent if someone infected recovers"""
    recovery_num = random.uniform(0,1)
    if recovery_num < recovery_rate:
        return True
    else:
        return False

def contact_indices(pop_size:int, source:int, contact_range:int) -> list:
    """This function determines which people come into contact with an
    individual who is infected, it takes 3 arguments pop_size determines
    how long the list will be, source determines the indice in the list that
    is infected, and cotnact_range is the amount of the indices that are
    subject to infection"""
    start = source - contact_range
    end = source + contact_range + 1
    if start < 0:
        start = 0
    if end > pop_size:
        end = pop_size
    contact_list = list(range(start,end))
    return contact_list

def apply_recoveries(population:list, recovery_percent:float) -> list:
    """docstring here takes a list of strings (population) and applies
    the recovery chance (recovery_percent) using the recover function
    while iterating through the population list.If the recovery works
    the I in the list becomes an R"""
    for item in range(len(population)):
        instance = population[item]
        if instance == 'I':
            instance = recover(recovery_percent)
            if instance == True:
                population[item] = 'R'
            else:
                population[item] = 'I'
    return population

def contact(population:list, source:int, contact_range:int, infect_chance:float) -> None:
    """Simulates an infected individual being in contact with other people
    the input takes 4 arguments, the population (population) the indice
    of the infected person (source), the range of exposed people (contact_range)
    and the chance of infection (infection_chance). The people who have been
    infected in the population is returned"""
    exposed_list = contact_indices(len(population), source, contact_range)
    for item in exposed_list:
        if population[item] == 'S':
            if infect(infect_chance) == True:
                population[item] = 'I'
    return

def apply_contacts(population:list, contact_range:int, infect_chance:float) -> None:
    """Simulates infected people coming into contact with other people, takes
    4 arguments which is a list for the population, the range of contact susceptibility
    and the chance of infection, doesn't return a specific object just alters
    the population list"""
    infected_list = []
    for item in range(len(population)):
        instance = population[item]
        if instance == 'I':
            infected_list.append(item) #Adds infected individuals indices to infected_list
    for item in infected_list:
        contact(population, item, contact_range, infect_chance)

    return 

def population_SIR_counts(population:list) -> dict:
    """Takes a list of strings representing the population and makes a count
    for individuals are infected, susceptible, and recovered. The function then
    returns a dictionary that stores the counts for the three categories"""
    status_counts = {'infected':0, 'susceptible':0, 'recovered':0}
    for item in population:
        if item == 'I':
            if 'infected' in status_counts:
                status_counts['infected'] += 1
        if item == 'S':
            if 'susceptible' in status_counts:
                status_counts['susceptible'] += 1
        if item == 'R':
            if 'recovered' in status_counts:
                status_counts['recovered'] += 1        
    return status_counts

def simulate_day(population:list, contact_range:int, infect_chance:float, recover_chance:float) -> None:
    """This function serves as a day for the disease, it takes 4 arguments,
    a list of strings for the population, the range of contact susceptibility,
    the change of infection, and the chance of recovery, it uses these arguments to
    use the apply_contacts and apply_recoveries functions to the list"""
    apply_contacts(population, contact_range, infect_chance)
    apply_recoveries(population, recover_chance)
    return

#FINAL FOUR FUNCTIONS
def initialize_population(pop_size:int) -> list:
    """This function takes an int as an argument that determines how long
    the returned list will be"""
    population = ['S'] * pop_size #List created with all individuals being marked as "Susceptible"
    population[0] = 'I' #Sets the first indice in the list to be "Infected"
    return population

def simulate_disease(pop_size:int, contact_range:int, infect_chance:float, recover_chance:float) -> list:
    """This function takes for argumants, an integer for the population size, the range
    of contact susceptibility, the chance of infection, and the chance of recovery.
    The function then uses the initialize_population function, the population_SIR_counts
    function, and the simulate_day function to return a list of dictionaries"""
    population = initialize_population(pop_size) #Creates a list the size of pop_size
    counts = population_SIR_counts(population) #Creates a dictionary recording the I, R, and S individuals and their counts
    all_counts = [counts]
    while counts['infected'] > 0: #Until the infected count reaches 0, the simulate day function will be applied and a new dictionary will be appended to the all_countz list
        simulate_day(population, contact_range, infect_chance, recover_chance)
        counts = population_SIR_counts(population)
        all_counts.append(counts)
    return all_counts #Returns a list of dictionaries

def peak_infections(all_counts:list) -> int:
    """This function takes one argument, a list of dictionaries, and returns the day that the infection count
    was the highest as an integer"""
    max_infections = 0
    for day in all_counts: #For all the dictonaries in the list, if the next dictionary had a higher value than the previous one, it becomes the new value for max_infections
        if day['infected'] > max_infections:
            max_infections = day['infected']
    return max_infections
        
def display_results(all_counts:list) -> None:
    """This function takes one argument, a list of the dictionaries for every day of the infection.
    it then prints out all of the data for each day and the peak infection day with the number of infections"""
    num_days = len(all_counts)
    print("Day".rjust(12) + "Susceptible".rjust(12) + "Infected".rjust(12) + "Recovered".rjust(12)) #Prints the labels for the data
    for day in range(num_days): #For every case a line containing all the relevant data will be printed
        line = str(day).rjust(12)
        line += str(all_counts[day]["susceptible"]).rjust(12)+'ඞ'
        line += str(all_counts[day]["infected"]).rjust(12) + '🤮'
        line += str(all_counts[day]["recovered"]).rjust(12) + '🐸'
        print(line)
    print("\nPeak Infections: {}".format(peak_infections(all_counts))) #Prints the day and count with the most infections, uses the peak_infections fucntion to do this
    
print("Simulate a disease here: ")
user_population_size = int(input("Population size: "))
user_contact_range = int(input("Contact Range: "))
user_infection_chance = float(input("Infection Chance: "))
user_recovery_chance = float(input("Recovery Chance: "))

counts = simulate_disease(user_population_size,user_contact_range,user_infection_chance,user_recovery_chance)
display_results(counts)
    
        
    
    
