% Rescale an image in a folder using sharpened edge detection

% Model parameters
%   - edge_ker_type: either 'Prewitt', 'Sobel', 'Sobel-Feldman' or 'Scharr'
%   - scale: multiplier to sacale each dimension, greater than 0
%   - sharpen_weight: amount to sharpen, greater than or equal to 1
%   - shift_weight: relative strength to use edge information in rescaling, greater than or equal to 0
edge_ker_type = 'Sobel-Feldman';
scale = 4;
sharpen_weight = 5;
shift_weight = 200;

% Initialize horizonal and vertical edge-detection and sharpen convolution kernels
if strcmp(edge_ker_type, 'Prewitt')
    vert_ker = [1, 0, -1; 1, 0, -1; 1, 0, -1];
    hori_ker = [1, 1, 1; 0, 0, 0; -1, -1, -1];
elseif strcmp(edge_ker_type, 'Sobel')
    vert_ker = [1, 0, -1; 2, 0, -2; 1, 0, -1];
    hori_ker = [1, 2, 1; 0, 0, 0; -1, -2, -1];
elseif strcmp(edge_ker_type, 'Sobel-Feldman')
    vert_ker = [3, 0, -3; 10, 0, -10; 3, 0, -3];
    hori_ker = [3, 10, 3; 0, 0, 0; -3, -10, -3];
elseif strcmp(edge_ker_type, 'Scharr')
    vert_ker = [47, 0, -47; 162, 0, -162; 47, 0, -47];
    hori_ker = [47, 162, 47; 0, 0, 0; -47, -162, -47];
else
    error('Error: Input of edge_ker_type invalid.')
end
sharp_ker = [0, (1 - sharpen_weight)/4, 0; (1 - sharpen_weight)/4,...
    sharpen_weight, (1 - sharpen_weight)/4; 0, (1 - sharpen_weight)/4, 0];

% Choose folder, load a jpg or png file in the folder
[file, path] = uigetfile({'*.jpg;*.png'; '*.*'});
if path ~= 0
    data = imread(strcat([path, file]));
else
    disp('No file selected.')
    return
end

% Find horizontal and vertical edges, combine to give all edges
vert_conv = zeros(size(data));
hori_conv = zeros(size(data));
depth = size(data, 3);
for i = 1:size(data, 3)
    vert_conv(:, :, i) = abs(conv2(data(:, :, i), vert_ker, 'same'));
    hori_conv(:, :, i) = abs(conv2(data(:, :, i), hori_ker, 'same'));
end
edge_mat = (vert_conv.^2 + hori_conv.^2).^0.5;

% Sharpen the edge data
sharp_edge_mat = zeros(size(edge_mat));
for i = 1:size(data, 3)
    sharp_edge_mat(:, :, i) = conv2(edge_mat(:, :, i), sharp_ker, 'same');
end
sharp_edge_mat = abs(sharp_edge_mat);

% Rescale the sharpened edge data for relative strength of use
shifted_mat = mean(shift_weight*sharp_edge_mat/max(sharp_edge_mat(:)) + ones(size(sharp_edge_mat)), 3);

% Change image resolution using linear interpolation of closest
% corresponding pixel values
row = round(scale*size(data, 1));
col = round(scale*size(data, 2));
row_old = size(data, 1);
col_old = size(data, 2);
new_data = zeros(row, col, depth);
d_data = double(data);  % needed since default data type is uint8
for i = 1:row
    for j = 1:col
        x = i/scale;        % x-value in original image
        dx = x - floor(x);
        y = j/scale;        % y-value in original image
        dy = y - floor(y);
        sum_total = zeros(depth, 1);
        weight_total = 0;
        % Add (x, y)-data to total if possible
        if (floor(x) >= 1) && (floor(y) >= 1) && (floor(x) <= row_old) && (floor(y) <= col_old)
            new_weight = (1 - dx)*(1 - dy)*shifted_mat(floor(x), floor(y));
            for k = 1:depth
                sum_total(k) = sum_total(k) + d_data(floor(x), floor(y), k)*new_weight;
            end
            weight_total = weight_total + new_weight;
        end
        % Add (x + 1, y)-data to total if possible
        if (floor(x) + 1 >= 1) && (floor(y) >= 1) && (floor(x) + 1 <= row_old) && (floor(y) <= col_old)
            new_weight = dx*(1 - dy)*shifted_mat(floor(x) + 1, floor(y));
            for k = 1:depth
                sum_total(k) = sum_total(k) + d_data(floor(x) + 1, floor(y), k)*new_weight;
            end
            weight_total = weight_total + new_weight;
        end
        % Add (x, y + 1)-data to total if possible
        if (floor(x) >= 1) && (floor(y) + 1 >= 1) && (floor(x) <= row_old) && (floor(y) + 1 <= col_old)
            new_weight = (1 - dx)*dy*shifted_mat(floor(x), floor(y) + 1);
            for k = 1:depth
                sum_total(k) = sum_total(k) + d_data(floor(x), floor(y) + 1, k)*new_weight;
            end
            weight_total = weight_total + new_weight;
        end
        % Add (x + 1, y + 1)-data to total if possible
        if (floor(x) + 1 >= 1) && (floor(y) + 1 >= 1) && (floor(x) + 1 <= row_old) && (floor(y) + 1 <= col_old)
            new_weight = dx*dy*shifted_mat(floor(x) + 1, floor(y) + 1);
            for k = 1:depth
                sum_total(k) = sum_total(k) + d_data(floor(x) + 1, floor(y) + 1, k)*new_weight;
            end
            weight_total = weight_total + new_weight;
        end
        % Store new data value
        if weight_total > 0
            for k = 1:depth
                new_data(i, j, k) = sum_total(k)/weight_total;
            end
        end
    end
end

% Convert double data back to uint8 for image export
new_data = uint8(new_data);
edge_mat = uint8(edge_mat);

% Export image and display info
imwrite(new_data, strcat([path, file]))
disp(strcat(['    Filename: ', file]))
disp(strcat(['    Old size: ', num2str(col_old), 'x', num2str(row_old)]))
disp(strcat(['    New size: ', num2str(col), 'x', num2str(row)]))