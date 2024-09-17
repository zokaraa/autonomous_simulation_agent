# At the end of the previous simulation script
distances = np.linalg.norm(earth_positions - asteroid_positions, axis=1)
np.savetxt('distance_data.txt', np.column_stack((time_array, distances)), header='Time(s) Distance(km)')
