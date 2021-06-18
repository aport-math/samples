% Constructs a plot of a graph using a force directed graph algorithm,
% includes a temperature cooling stabilizing term
% Done initially in 3D, then squished to 2D
% Force for v4 is determined only by graph-theoretic distance

% Load the data files
[data_filename, data_pathname] = uigetfile({'*.txt'}, 'Select Data File');
if data_filename ~= 0       % if the OK button was pressed
    filename = strcat(data_pathname, data_filename);
    try
        % Load the raw data
        simplex_mat = reduce_matrix(load(filename), 0);
        disp(strcat([data_filename, ' loaded']));
    catch
        error('Error: The data file failed to load.')
    end
else
    % Generate a random one if cancel was pressed
    num_simplices = 4;      % number of simplcies to use (i.e. number of rows)
    num_vertices = 30;       % number of vertices to use (i.e. number of columns)
    p_connection = 0.2;     % probability of a connection between vertices
    simplex_mat = reduce_matrix(rand(num_simplices, num_vertices) < p_connection, 0);
end
num_simplices = size(simplex_mat, 1);
num_vertices = size(simplex_mat, 2);

% Model parameters
edge_len = 0.7;             % desired ideal edge length
force_scale = 4;            % scale of forces to apply to vertices
stable_thresh = 0.0001;     % stability threshold required to terminate

time_step = 0.02;           % duration of time step in simulation
min_time = 4;               % min time to run simulation in 3D
max_time = 15;              % max time to run simulation in 3D
min_flat_time = 2;          % min time to run the flattening simulation
max_flat_time = 4;          % max time to run the flattening simulation
cluster_spacing = 5;        % scale of spacing between cluster centers
draw_scale = 0.75;          % final percent of box size to draw with
temp_start = 0.4;           % max force size in a time step, as a percent of edge_len
temp_decay = 1.5;           % rate at which to decay the temperature

% Constructed variables
normed_force_scale = edge_len*force_scale;      % normalize force based on edge length

% Create adjacency matrix based on simplex_mat
adj_mat = zeros(num_vertices, num_vertices);    % adjacency matrix
for i = 1:num_simplices
    for j = 1:num_vertices - 1
        for k = j + 1:num_vertices
            if (simplex_mat(i, j) == 1) && (simplex_mat(i, k) == 1)
                adj_mat(j, k) = 1;
                adj_mat(k, j) = 1;
            end
        end
    end
end

% Determine clusters of simplex_mat
clusters = cell(num_vertices, 1);
for i = 1:num_vertices
    clusters{i} = [i]; %#ok<NBRAK>
end
for i = 1:num_vertices - 1
    for j = i + 1:num_vertices
        if adj_mat(i, j) == 1
            % Search for indices
            for k = 1:length(clusters)
                if any(i == clusters{k})
                index_i = k;
                    break
                end
            end
            for k = 1:length(clusters)
                if any(j == clusters{k})
                index_j = k;
                    break
                end
            end
            
            % Merge the clusters
            if index_i ~= index_j
                clusters{index_i} = [clusters{index_i}, clusters{index_j}];
                clusters(index_j) = [];
            end
        end
    end
end

% Compute the graph distance between each node by cluster
dist_mat = adj_mat;
loop_mat = adj_mat;
for i = 2:num_vertices - 1
    loop_mat = loop_mat*adj_mat;
    for j = 1:num_vertices
        for k = 1:num_vertices
            if (j ~= k) && (dist_mat(j, k) == 0) && (loop_mat(j, k) ~= 0)
                dist_mat(j, k) = i;
            end
        end
    end
end

% Compute the number of rows of columns for the clusters
num_clusters = length(clusters);
num_row = floor(sqrt(num_clusters));
if num_row^2 == num_clusters
    num_col = num_row;
    square_flag = 1;
else
    num_row = ceil((sqrt(4*num_clusters + 1) - 1)/2);
    if num_row^2 >= num_clusters
        num_col = num_row;
    else
        num_col = num_row + 1;
    end
    square_flag = 0;
end

% Determine the centers of the clusters
starting_centers = zeros(num_clusters, 3);             % positional data
counter = 1;
for i = 1:num_col
    for j = 1:num_row
        if counter <= num_clusters
            starting_centers(counter, 1) = cluster_spacing*edge_len*(i - num_col/2);
            if (square_flag == 1) || (i < num_col)
                starting_centers(counter, 2) = cluster_spacing*edge_len*(j - num_row/2);
            else
                starting_centers(counter, 2) = cluster_spacing*edge_len*(j - num_row/2) + ...
                    (num_row*num_col - num_clusters)*cluster_spacing*edge_len/2;
            end
            counter = counter + 1;
        else
            break
        end
    end
end

% Construct initial positional data based on clustering
pos_data = edge_len/2*rand(num_vertices, 3);             % positional data
for i = 1:num_clusters
    cluster_i = clusters{i};
    for j = 1:length(cluster_i)
        pos_data(cluster_i(j), :) = pos_data(cluster_i(j), :) + starting_centers(i, :);
    end
end

% Run the simulation in 3D
disp('>>> Running main simulation in 3D...')
figure
tic
temp_current = edge_len*temp_start;
stable = 0;
while ((toc < min_time) || (stable == 0)) && (toc < max_time)
    % Start timer
    t_0 = toc;
    
    % Generate the force data
    force_data = zeros(num_vertices, 3);
    for i = 1:num_vertices - 1
        % Repel/attract vertices
        for j = i + 1:num_vertices
            diff_ij = pos_data(i, :) - pos_data(j, :);
            norm_ij = norm(diff_ij);
            if norm_ij > 0
                if norm_ij < edge_len*dist_mat(i, j)        % repel if too close
                    force_data(i, :) = force_data(i, :) +...
                        normed_force_scale*diff_ij/norm_ij*(edge_len*dist_mat(i, j) /norm_ij - 1);
                    force_data(j, :) = force_data(j, :) -...
                        normed_force_scale*diff_ij/norm_ij*(edge_len*dist_mat(i, j) /norm_ij - 1);
                else                                        % attract if too far
                    force_data(i, :) = force_data(i, :) -...
                        normed_force_scale*diff_ij/norm_ij*(norm_ij/(edge_len*dist_mat(i, j)) - 1);
                    force_data(j, :) = force_data(j, :) +...
                        normed_force_scale*diff_ij/norm_ij*(norm_ij/(edge_len*dist_mat(i, j))  - 1);
                end
            end
        end
    end
    
    % Determine if simulation stable based on length changes
    mean_force = mean(sqrt(sum(force_data.^2, 1)));
    new_pos_data = pos_data + time_step*force_data;
    length_changes = zeros(num_vertices, num_vertices);
    for i = 1:num_vertices - 1
        for j = i + 1:num_vertices
            if adj_mat(i, j) == 1
                len_old = norm(pos_data(i, :) - pos_data(j, :));
                len_new = norm(new_pos_data(i, :) - new_pos_data(j, :));
                len_diff = len_new - len_old;
                length_changes(i, j) = len_diff;
                length_changes(j, i) = len_diff;
            end
        end
    end
    sum_non_zero = 0;
    count_non_zero = 0;
    for i = 1:num_vertices - 1
        for j = i + 1:num_vertices
            sum_non_zero = sum_non_zero + length_changes(i, j);
            count_non_zero = count_non_zero + 1;
        end
    end
    if count_non_zero == 0
        mean_non_zero = 0;
    else
        mean_non_zero = sum_non_zero/count_non_zero;
    end
    if mean_non_zero < stable_thresh*edge_len*force_scale
        stable = 1;
    end
    
    % Update positional data
    for i = 1:num_vertices
        force_i = force_data(i, :);
        norm_i = norm(force_i);
        if norm_i > 0
            pos_data(i, :) = pos_data(i, :) + force_i/norm_i*min(time_step*norm_i, temp_current);
        end
    end
    x_min = min(pos_data(:, 1));
    x_max = max(pos_data(:, 1));
    x_diff = 0.2*(x_max - x_min);
    y_min = min(pos_data(:, 2));
    y_max = max(pos_data(:, 2));
    y_diff = 0.2*(y_max - y_min);
    
    % Update the temperature
    temp_current = edge_len*temp_start/(1 + toc)^temp_decay;
    
    % Update the plot
    t_1 = toc;
    pause(time_step - t_1 + t_0)
    scatter(pos_data(:, 1), pos_data(:, 2))
    hold on
    for i = 1:num_vertices - 1
        for j = i + 1:num_vertices
            if adj_mat(i, j) == 1
                plot([pos_data(i, 1), pos_data(j, 1)], [pos_data(i, 2), pos_data(j, 2)], 'b')
            end
        end
    end
    hold off
    axis([x_min - x_diff, x_max + x_diff, y_min - y_diff, y_max + y_diff])
    set(gca, 'visible', 'off')
    pause(0.0001)
end

% Choose the best coordinates to project with for each cluster
best_dims = zeros(num_clusters, 2);
for index = 1:num_clusters
    % Initialize
    vertices_to_use = clusters{index};
    num_vertices_used = length(vertices_to_use);
    stop_flag = 0;
    flag_array = zeros(3, 1);
    flag_array(end) = 1;
    flag_array(end - 1) = 1;
    best_fitness = 0;
    while stop_flag == 0
        % Test if complete
        if (flag_array(1) == 1) && (flag_array(2) == 1)
            stop_flag = 1;
        end
    
        % Only proceed if two dimensions selected
        if sum(flag_array) ==  2
            % Extract the dims to use
            dims_to_use = zeros(1, 2);
            counter = 0;
            for i = 1:3
                if flag_array(i) == 1
                    counter = counter + 1;
                    dims_to_use(counter) = i;
                    if counter == 2
                        break
                    end
                end
            end
    
            % Compute the fitness of this projection using colinearity
            fitness = 0;
            for i = 1:num_vertices_used
                i0 = vertices_to_use(i);
                for j = 1:num_vertices_used - 1
                    j0 = vertices_to_use(j);
                    if i0 ~= j0
                        diff_ij = pos_data(i0, dims_to_use) - pos_data(j0, dims_to_use);
                        for k = j + 1:num_vertices_used
                            k0 = vertices_to_use(k);
                            if (i0 ~= k0) && (adj_mat(j0, k0) == 1)
                                diff_kj = pos_data(k0, dims_to_use) - pos_data(j0, dims_to_use);
                                norm_kj = norm(diff_kj);
                                scalar_ijk = sum(diff_ij.*diff_kj)/norm_kj;
                                para_ijk = (scalar_ijk/norm_kj)*diff_kj;
                                orth_ijk = diff_ij - para_ijk;
                                norm_orth_ijk = norm(orth_ijk);
                                fitness = fitness + 1 - exp(-(norm_orth_ijk/edge_len)^2);
                            end
                        end
                    end
                end
            end
    
            % Keep track of the best fitness
            if fitness > best_fitness
                best_fitness = fitness;
                best_dims(index, :) = dims_to_use;
            end
        end
    
        % Iterate to the next flag_array
        flag_array(end) = flag_array(end) + 1;
        for i = 3:-1:2
            if flag_array(i) == 2
                flag_array(i) = 0;
                flag_array(i - 1) = flag_array(i - 1) + 1;
            else
                break
            end
        end
    end
end

% Correct for any entries of all zeros, occurs because of singletons
for i = 1:num_clusters
    if (best_dims(i, 1) == 0) || (best_dims(i, 2) == 0)
        best_dims(i, 1) = 1;
        best_dims(i, 2) = 2;
    end
end

% Store the current vertex coordinates
x_data_current = pos_data(:, 1);
y_data_current = pos_data(:, 2);

% Change the coordinates to the best choices
for index = 1:num_clusters
    % Initialize
    vertices_to_use = clusters{index};
    num_vertices_used = length(vertices_to_use);
    new_coordinates = [best_dims(index, :), setdiff([1, 2, 3], best_dims(index, :))];
    
    % Swap the coordinates
    pos_data(vertices_to_use, :) = pos_data(vertices_to_use, new_coordinates)...
        - starting_centers(index, new_coordinates) + starting_centers(index, :);
end


% Create an animation switching to the best coordinates
disp('>>> Shifting to best coordinates...')
for i = 0:0.05:1
    % Start timer
    t_0 = toc;
    
    % Create new frame data
    x_data_to_view = x_data_current*(1 - i) + pos_data(:, 1)*i;
    y_data_to_view = y_data_current*(1 - i) + pos_data(:, 2)*i;
    
    % Draw the new frame
    scatter(x_data_to_view, y_data_to_view)
    hold on
    for j = 1:num_vertices - 1
        for k = j + 1:num_vertices
            if adj_mat(j, k) == 1
                plot([x_data_to_view(j), x_data_to_view(k)], [y_data_to_view(j), y_data_to_view(k)], 'b')
            end
        end
    end
    hold off
    x_min = min(x_data_to_view);
    x_max = max(x_data_to_view);
    x_diff = 0.2*(x_max - x_min);
    y_min = min(y_data_to_view);
    y_max = max(y_data_to_view);
    y_diff = 0.2*(y_max - y_min);
    axis([x_min - x_diff, x_max + x_diff, y_min - y_diff, y_max + y_diff])
    set(gca, 'visible', 'off')
    
    % Stop timer and wait
    t_1 = toc;
    pause(max([time_step - t_1 + t_0, 0.0001]))
end

% Run the flattening simulation
disp('>>> Running flattening simulation...')
tic
temp_current = edge_len*temp_start;
flat_time = 0;
stable = 0;
while (flat_time < max_flat_time) && (stable == 0)
    % Start timer
    t_0 = toc;
    
    % Create the next time step
    flat_time = flat_time + time_step;
    
    % Partially flatten the data
    if flat_time >= 1
        pos_data(:, 3) = 0;
    else
        pos_data(:, 3) = pos_data(:, 3)*(1 - flat_time)/(1 - flat_time + time_step);
    end
    
    % Generate the force data
    force_data = zeros(num_vertices, 3);
    for i = 1:num_vertices - 1
        % Repel/attract vertices
        for j = i + 1:num_vertices
            diff_ij = pos_data(i, [1, 2]) - pos_data(j, [1, 2]);
            norm_ij = norm(diff_ij);
            if norm_ij > 0
                if norm_ij < edge_len*dist_mat(i, j)        % repel if too close
                    force_data(i, [1, 2]) = force_data(i, [1, 2]) +...
                        normed_force_scale*diff_ij/norm_ij*(edge_len*dist_mat(i, j)/norm_ij - 1);
                    force_data(j, [1, 2]) = force_data(j, [1, 2]) -...
                        normed_force_scale*diff_ij/norm_ij*(edge_len*dist_mat(i, j)/norm_ij - 1);
                else                                        % attract if too far
                    force_data(i, [1, 2]) = force_data(i, [1, 2]) -...
                        normed_force_scale*diff_ij/norm_ij*(norm_ij/(edge_len*dist_mat(i, j)) - 1);
                    force_data(j, [1, 2]) = force_data(j, [1, 2]) +...
                        normed_force_scale*diff_ij/norm_ij*(norm_ij/(edge_len*dist_mat(i, j))  - 1);
                end
            end
        end
    end
    
    % Determine if simulation stable based on length changes
    if flat_time >= min_flat_time
        mean_force = mean(sqrt(sum(force_data.^2, 1)));
        new_pos_data = pos_data + time_step*force_data;
        length_changes = zeros(num_vertices, num_vertices);
        for i = 1:num_vertices - 1
            for j = i + 1:num_vertices
                if adj_mat(i, j) == 1
                    len_old = norm(pos_data(i, :) - pos_data(j, :));
                    len_new = norm(new_pos_data(i, :) - new_pos_data(j, :));
                    len_diff = len_new - len_old;
                    length_changes(i, j) = len_diff;
                    length_changes(j, i) = len_diff;
                end
            end
        end
        sum_non_zero = 0;
        count_non_zero = 0;
        for i = 1:num_vertices - 1
            for j = i + 1:num_vertices
                sum_non_zero = sum_non_zero + length_changes(i, j);
                count_non_zero = count_non_zero + 1;
            end
        end
        if count_non_zero == 0
            mean_non_zero = 0;
        else
            mean_non_zero = sum_non_zero/count_non_zero;
        end
        if mean_non_zero < stable_thresh*edge_len*force_scale
            stable = 1;
        end
    end
    
    % Update positional data
    for i = 1:num_vertices
        force_i = force_data(i, :);
        norm_i = norm(force_i);
        if norm_i > 0
            pos_data(i, :) = pos_data(i, :) + force_i/norm_i*min(time_step*norm_i, temp_current);
        end
    end
    x_min = min(pos_data(:, 1));
    x_max = max(pos_data(:, 1));
    x_diff = 0.2*(x_max - x_min);
    y_min = min(pos_data(:, 2));
    y_max = max(pos_data(:, 2));
    y_diff = 0.2*(y_max - y_min);
    
    % Update the temperature
    temp_current = edge_len*temp_start/(1 + toc)^(temp_decay/2);
    
    % Update the plot
    t_1 = toc;
    pause(time_step - t_1 + t_0)
    scatter(pos_data(:, 1), pos_data(:, 2))
    hold on
    for i = 1:num_vertices - 1
        for j = i + 1:num_vertices
            if adj_mat(i, j) == 1
                plot([pos_data(i, 1), pos_data(j, 1)], [pos_data(i, 2), pos_data(j, 2)], 'b')
            end
        end
    end
    hold off
    axis([x_min - x_diff, x_max + x_diff, y_min - y_diff, y_max + y_diff])
    set(gca, 'visible', 'off')
    pause(0.0001)
end

% Store the current vertex coordinates
x_data_current = pos_data(:, 1);
y_data_current = pos_data(:, 2);

% Compute the centers of the clusters in first two dimensions
cluster_centers = zeros(num_clusters, 2);
for i = 1:num_clusters
    cluster_i = clusters{i};
    for j = 1:length(cluster_i)
        cluster_centers(i, 1) = cluster_centers(i, 1) +...
            pos_data(cluster_i(j), 1)/length(cluster_i);
        cluster_centers(i, 2) = cluster_centers(i, 2) +...
            pos_data(cluster_i(j), 2)/length(cluster_i);
    end
end

% Compute the radius of each projected cluster
cluster_radii = zeros(num_clusters, 1);
for i = 1:num_clusters
    cluster_i = clusters{i};
    for j = 1:length(cluster_i) - 1
        for k = j + 1:length(cluster_i)
            diff_jk = pos_data(cluster_i(j), [1, 2]) - pos_data(cluster_i(k), [1, 2]);
            norm_jk = sqrt(sum(diff_jk.^2));
            if cluster_radii(i) < norm_jk
                cluster_radii(i) = norm_jk;
            end
        end
    end
end

% Shift the results to the best positions
x_data = zeros(num_vertices, 1);
y_data = zeros(num_vertices, 1);
for i = 1:num_clusters
    cluster_i = clusters{i};
    for j = 1:length(cluster_i)
        if cluster_radii(i) > 0
            x_data(cluster_i(j)) = (pos_data(cluster_i(j), 1) - cluster_centers(i, 1))*...
                draw_scale*cluster_spacing*edge_len/cluster_radii(i) + starting_centers(i, 1);
            y_data(cluster_i(j)) = (pos_data(cluster_i(j), 2) - cluster_centers(i, 2))*...
                draw_scale*cluster_spacing*edge_len/cluster_radii(i) + starting_centers(i, 2);
        else
            x_data(cluster_i(j)) = pos_data(cluster_i(j), 1) - cluster_centers(i, 1) + starting_centers(i, 1);
            y_data(cluster_i(j)) = pos_data(cluster_i(j), 2) - cluster_centers(i, 2) + starting_centers(i, 2);
        end
    end
end

% Create an animation to the final figure
disp('>>> Rescaling to final figure...')
for i = 0:0.05:1
    % Start timer
    t_0 = toc;
    
    % Create new frame data
    x_data_to_view = x_data_current*(1 - i) + x_data*i;
    y_data_to_view = y_data_current*(1 - i) + y_data*i;
    
    % Draw the new frame
    scatter(x_data_to_view, y_data_to_view)
    hold on
    for j = 1:num_vertices - 1
        for k = j + 1:num_vertices
            if adj_mat(j, k) == 1
                plot([x_data_to_view(j), x_data_to_view(k)], [y_data_to_view(j), y_data_to_view(k)], 'b')
            end
        end
    end
    hold off
    x_min = min(x_data_to_view);
    x_max = max(x_data_to_view);
    x_diff = 0.2*(x_max - x_min);
    y_min = min(y_data_to_view);
    y_max = max(y_data_to_view);
    y_diff = 0.2*(y_max - y_min);
    axis([x_min - x_diff, x_max + x_diff, y_min - y_diff, y_max + y_diff])
    set(gca, 'visible', 'off')
    
    % Stop timer and wait
    t_1 = toc;
    pause(max([time_step - t_1 + t_0, 0.0001]))
end

% Plot the final figure
scatter(x_data, y_data)
hold on
for i = 1:num_vertices - 1
    for j = i + 1:num_vertices
        if adj_mat(i, j) == 1
            plot([x_data(i), x_data(j)], [y_data(i), y_data(j)], 'b')
        end
    end
end
hold off
x_min = min(x_data);
x_max = max(x_data);
x_diff = 0.2*(x_max - x_min);
y_min = min(y_data);
y_max = max(y_data);
y_diff = 0.2*(y_max - y_min);
axis([x_min - x_diff, x_max + x_diff, y_min - y_diff, y_max + y_diff])
set(gca, 'visible', 'off')
