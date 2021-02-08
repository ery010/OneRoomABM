## positional code: replace w/ square/circular desks TODO

def init_positions(floor_area, n_students):
    # generate size of room based on circular/square desks
    positions = {}
    # grid desks
    rows = int(math.sqrt(n_students))
    count = 0
    for i in range(rows):
        for j in range(rows):
            positions[count] = [i, j]
            count += 1
    inf_index = random.sample(set(range(25)), 2)
    uninf_index = list(range(25))
    inf_array = []


    # double check this
    for i in inf_index:
        uninf_index.remove(i)
        inf_array.append(i)
    return uninf_index, inf_index, inf_array, positions


def droplet_infect(infect_id, uninfect_id, infected):
    distance = get_distance(infect_id, uninfect_id, student_pos)
    print(infected)
    time = infected[infect_id]
    transmission_baseline = infective_df[infective_df.x == -1 * time]['gamma']
    distance_multiplier = get_dist_multiplier(distance)
    return transmission_baseline * distance_multiplier

def return_aerosol_transmission_rate(floor_area, room_height,
                            air_exchange_rate,
                            aerosol_filtration_eff, relative_humidity, breathing_flow_rate,
                            exhaled_air_inf, max_viral_deact_rate, mask_passage_prob,
                            max_aerosol_radius=2, primary_outdoor_air_fraction=0.2):

    mean_ceiling_height_m = mean_ceiling_height * 0.3048 #m3
    room_vol = floor_area * mean_ceiling_height  # ft3
    room_vol_m = 0.0283168 * room_vol  # m3

    fresh_rate = room_vol * air_exchange_rate / 60  # ft3/min
    recirc_rate = fresh_rate * (1/primary_outdoor_air_fraction - 1)  # ft3/min
    air_filt_rate = aerosol_filtration_eff * recirc_rate * 60 / room_vol  # /hr
    eff_aerosol_radius = ((0.4 / (1 - relative_humidity)) ** (1 / 3)) * max_aerosol_radius
    viral_deact_rate = max_viral_deact_rate * relative_humidity
    sett_speed = 3 * (eff_aerosol_radius / 5) ** 2  # mm/s
    sett_speed = sett_speed * 60 * 60 / 1000  # m/hr
    conc_relax_rate = air_exchange_rate + air_filt_rate + viral_deact_rate + sett_speed / mean_ceiling_height_m  # /hr
    airb_trans_rate = ((breathing_flow_rate * mask_passage_prob) ** 2) * exhaled_air_inf / (room_vol_m * conc_relax_rate)

    return airb_trans_rate #This is mean number of transmissions per hour between pair of infected / healthy individuals

def get_distance(infect_id, uninfect_id, student_pos):
    x1y1 = student_pos[infect_id]
    x2y2 = student_pos[uninfect_id]
    return math.sqrt(((x2y2[0]-x1y1[0])**2) + ((x2y2[1] - x1y1[1])**2))

def get_dist_multiplier(distance):
    return distance * chu_distance_curve




def one_room(input_dir, output_dir):
    num_out_test = 0

    ################ TODO ###############

    uninf_index, inf_index, inf_array, student_pos = init_positions(900, 25)

    # setup variables and functions# output graphs
    # countdown until symptoms appear: probability curve
    shape, loc, scale =  (0.6432659248014824, -0.07787673726582335, 4.2489459496009125)
    x = np.linspace(0, 17, 1000)
    countdown_curve = stats.lognorm(s=shape, loc=loc, scale=scale)

    infected = {i: int(np.round(stats.lognorm.rvs(shape, loc, scale, size=1)[0], 0)) for i in inf_index}

    # bound the days for overflow errors
    for i in infected:
        if infected[i] > 18:
            infected[i] = 18
        if infected[i] < -10:
            infected[i] = -10
    print(infected)
    # create infectiveness reference dataframe
    shape, loc, scale = (20.16693271833812, -12.132674385322815, 0.6322296057082886)
    x = np.linspace(-10, 8, 19)
    infective_df = pd.DataFrame({'x': list(x), 'gamma': list(stats.gamma.pdf(x, a=shape, loc=loc, scale=scale))})

    uninfected = {i: 0 for i in uninf_index}
    chu_distance_curve = 1/2.02

    default_params = {floor_area: 900,
     mean_ceiling_height: 12,
     air_exchange_rate: 3,
     primary_outdoor_air_fraction: 0.2,
     aerosol_filtration_eff: 0,
     relative_humidity: 0.69,
     breathing_flow_rate: 0.5,
     max_aerosol_radius: 2,
     exhaled_air_inf: 30,
     max_viral_deact_rate: 0.3,
     mask_passage_prob: 0.1,
    risk_tolerance: 0.1}


    ######### TODO ###################

    # loop through day
    days = 1
    classes = 3
    steps = 1 # TODO: replace this with breathing changes for different periods of time?
    step_count = 0

    num_infected = 2

    # Aerosol transmission in this room (assumes well-mixed room)
    air_transmission = return_aerosol_transmission_rate(floor_area, mean_ceiling_height,
                            air_exchange_rate,
                            aerosol_filtration_eff, relative_humidity, breathing_flow_rate,
                            exhaled_air_inf, max_viral_deact_rate, mask_passage_prob,
                            max_aerosol_radius=2, primary_outdoor_air_fraction=0.2)


    for i in range(days):

        # Loop through classes in each day (3 classes)
        for c in range(classes):

            # Loop through 5 minute steps in each class
            for s in range(steps):
                step_count += 1

                ## Droplet Infection
                # Loop through infected students
                for i_student in inf_index:
                    # Loop through uninfected and calculate likelihood of infection
                    for u_student in uninf_index:
                        transmission = droplet_infect(i_student, u_student, infected).iloc[0]
                        if np.random.choice([True, False], p=[transmission, 1-transmission]):


                            # add u to infected
                            num_out_test += 1
                            inf_array.append(u_student)
                            # also calculate time until symptoms for u_studnet

                            uninf_index.remove(u_student)


        ## Aerosol Infection
        # Loop through infected and uninfected for pairwise calculations

        #### TODO 2/8 ####################
        for i in inf_index:

            for u in uninf_index:
#                 return_aerosol_transmission_rate()
                pass

    out = 2 # count number students in inf_index
    print('this is the number of infected students')
    print(inf_array)
    return len(inf_array)
