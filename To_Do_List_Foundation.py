'''The barebones version of an app I want to do'''

import pandas as pd

def initial_questions():
    while True:
        prod_days = input("How many days do you give to work on your projects?: ")
        prod_hours = input("How many hours a day do you often work?: ")

        # verify if integers
        try:
            prod_days = int(prod_days)
            prod_hours = int(prod_hours)
            break
        except ValueError:
            print("Please type in numbers for days and hours!")
        
    return prod_days, prod_hours

def main_tasks():
    # get main task name
    # ask for other project names or proceed to sub tasks
    main_tasks_list = []  # empty list

    while True:
        main_task_name = input("What's your project or task called?: ")
        main_tasks_list.append({'task_name': main_task_name, 'sub_tasks': []})

        # continue adding or proceed
        confirmation = input("Are there other projects you'd like to include? y/n: ")
        if confirmation == 'n':
            break
        elif confirmation != 'y':
            print("Only y/n please.")

    return main_tasks_list

def sub_tasks(main_tasks_list):
    for main_task in main_tasks_list:
        while True:
            sub_task_name = input(f"What's your sub-task for '{main_task['task_name']}?: ")
            priority = input("How important is this (High/Medium/Low): ")
            estimated_time = input("How many hours do you need for this?: ")

            main_task['sub_tasks'].append({
                'sub_task_name': sub_task_name,
                'priority': priority,
                'estimated_time': estimated_time
            })

            confirmation = input("Do you want to add more tasks? y/n: ")
            if confirmation != 'y':
                break

    return main_tasks_list


def feasibility(main_tasks_list,  prod_days, prod_hours):
    # Focuses on the amount of tasks in a main project and its feasibility
    # Using the days of productivity and hours of productivity 
    # Considering the priority and the estimate time of completion
    # Show feasibility for each main tasks

    feasibility_results = []

    for task in main_tasks_list:
        total_productivity = prod_days * prod_hours 
        total_estimated_hours = sum(int(sub_tasks['estimated_time']) for sub_tasks in task['sub_tasks'])
        total_tasks = len(task['sub_tasks'])

        # priority weights 
        priority_weights = {
            'High': 3,
            'Medium': 2,
            'Low': 1
        }
        
        # calculate total weight per priority
        priority_weight_high = sum(priority_weights['High'] for sub_task in task['sub_tasks'] if sub_task['priority'] == 'High')
        priority_weight_mid = sum(priority_weights['Medium'] for sub_task in task['sub_tasks'] if sub_task['priority'] == 'Medium')
        priority_weight_low = sum(priority_weights['Low'] for sub_task in task['sub_tasks'] if sub_task['priority'] == 'Low')
        total_priority_weight = priority_weight_high + priority_weight_mid + priority_weight_low


        # feasibility score
        if total_tasks > 0:
            feasibility_score = (total_productivity - total_estimated_hours) / (total_priority_weight * total_tasks) 
        else:
            feasibility_score = 0

        # feasibility rating
        if feasibility_score >= 0.8:
            feasibilty_rating = "This is doable (green)"
        elif feasibility_score >= 0.5:
            feasibilty_rating = "Maybe you can do this (yellow)"
        else:
            feasibilty_rating = "I advice you to replan (red)"

        feasibility_results.append({
            'task_name': task['task_name'],
            'feasibiliy_rating': feasibilty_rating
        })

    return feasibility_results
    

def display_projects(main_tasks_list):
    data = {task['task_name']: [sub_task['sub_task_name'] for sub_task in task['sub_tasks']] for task in main_tasks_list}    
    df = pd.DataFrame.from_dict(data, orient='index').transpose()
    print("\nYour Projects")
    print(df)


def main():
    prod_days, prod_hours = initial_questions() # gather important data from users
    main_tasks_list = main_tasks()
    sub_tasks_list = sub_tasks(main_tasks_list)
    feasibility_ratings = feasibility(main_tasks_list, prod_days, prod_hours)

    # diplay main tasks, sub-tasks, and feasibility rating 
    # WIP
    display_projects(main_tasks_list) 
    print(feasibility_ratings)


if __name__ == '__main__':
    main()