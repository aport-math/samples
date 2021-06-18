# Import needed packages
println()
println(">>> IMPORTING PACKAGES...")
t_0 = time()
using Plots: plot, plot!, savefig, xlabel!, ylabel!
t_1 = time()
println(">>> PACKAGES IMPORTED, ", round(t_1 - t_0, digits = 2), " SECONDS ELAPSED")

# Model parameters
alpha = 1                   # value at zero
beta = 1                    # derivative at zero
L_values = [2, 4, 8, 16]    # limiting values to use
scale = 0.25                # amount of noise
smth_val = 0.1              # smooth value

# Generate x-data
println(">>> GENERATING DATA...")
x_min = -2
x_max = 1
sub_div = 10*(x_max - x_min)
x_values = zeros(Float64, sub_div + 1)
for i = 1:sub_div + 1
    x_values[i] = x_min + (i - 1)*(x_max - x_min)/sub_div
end

# Generate y-data
y_values = zeros(Float64, sub_div + 1, length(L_values) + 1)
y_values[:, 1] = alpha.*exp.(x_values.*(beta/alpha))
for i = 1:length(L_values)
    c = L_values[i]/alpha - 1
    r = beta/(alpha*(L_values[i] - alpha))
    y_values[:, i + 1] = L_values[i]./(1 .+ c.*exp.(x_values.*(-r*L_values[i])))
end
y_values .+= (scale*(x_max - x_min)/sub_div).*(rand(sub_div + 1, length(L_values) + 1).*2 .- 1)

# Generate the shortened y-data and derivative data
y_values_short = zeros(Float64, sub_div, length(L_values) + 1)
y_values_diff = zeros(Float64, sub_div, length(L_values) + 1)
for i = 1:sub_div
    for j = 1:length(L_values) + 1
        y_values_short[i, j] = 0.5*(y_values[i + 1, j] + y_values[i, j])
        y_values_diff[i, j] = y_values[i + 1, j] - y_values[i, j]
    end
end

# Smooth the data
y_diff_smooth = zeros(Float64, sub_div, length(L_values) + 1)
for i = 1:sub_div
    for j = 1:length(L_values) + 1
        numerator = 0
        denominator = 0
        for k = 1:sub_div
            numerator += y_values_diff[k, j]*exp(-(y_values_short[i, j] - y_values_short[k, j])^2/smth_val)
            denominator += exp(-(y_values_short[i, j] - y_values_short[k, j])^2/smth_val)
        end
        y_diff_smooth[i, j] = numerator/denominator
    end
end

# Create the legend labels
legend_labels = Array{String, 2}(undef, 1, length(L_values) + 1)
legend_labels[1, 1] = "Unlimited"
for i = 1:length(L_values)
    legend_labels[1, i + 1] = "Limited L = "*string(L_values[i])
end

# Plot the x-data vs y-data
println(">>> PLOTTING X vs Y DATA...")
plot(x_values, y_values[:, 1], label = legend_labels[1, 1])
for i = 1:length(L_values)
    plot!(x_values, y_values[:, i + 1], label = legend_labels[1, i + 1])
end
plot!(legend = :topleft, title = "X vs Y data")
xlabel!("x")
ylabel!("y")

# Change the working directory to the file directory
cd(dirname(@__FILE__))

# Save the plot
println(">>> SAVING FIGURE 1...")
savefig("x_vs_y.png")

# Plot the y-data vs y'-data
plot(y_values_short[:, 1], y_values_diff[:, 1], label = legend_labels[1, 1])
for i = 1:length(L_values)
    plot!(y_values_short[:, i + 1], y_values_diff[:, i + 1], label = legend_labels[1, i + 1])
end
plot!(legend = :topleft, title = "Y vs Y' data")
xlabel!("y")
ylabel!("y'")

# Save the plot
println(">>> SAVING FIGURE 2...")
savefig("y_vs_y-diff.png")

# Plot the y-data vs smoothed y'-data
plot(y_values_short[:, 1], y_diff_smooth[:, 1], label = legend_labels[1, 1])
for i = 1:length(L_values)
    plot!(y_values_short[:, i + 1], y_diff_smooth[:, i + 1], label = legend_labels[1, i + 1])
end
plot!(legend = :topleft, title = "Y vs Y' data smoothed")
xlabel!("y")
ylabel!("y'")

# Save the plot
println(">>> SAVING FIGURE 3...")
savefig("y_vs_y-diff-smooth.png")
println()