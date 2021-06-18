function steenrod(poly_array; mod_prime = 2, degrees = 0:maximum(sum(poly_array[:, 2:end], dims = 2)))
    # Note: output is an array if degrees is a single number, but a
    # cell array if it is more than one number. Thus, thus function can be
    # nested if one shift is applied at a time because power_array must be a
    # non-cell array
    
    # - poly_array should be a row array of integers >= 1, must have at least
    #   2 entries (first column non-zero but doesn't have to be integral),
    #   (actually can have 0's but doesn't add anything)
    # - degrees should be a single row array of  integer >= 0 (will be empty
    #   when shift is greater than sum(power_array))
    # - mod_prime should be a prime number, if down want to mod then use Inf
    
    # - If poly_array = [c0, c1, ..., cn] and shift = i, returns
    #   Sq^i(c0*x1^c1*...*xn^cn), which is the degree (c1 + ... + cn + i) part
    #   of c0*(x1 + x1^mod_prime)^c1*...(xn + xn^mod_prime)^cn (use 2 if mod_prime = Inf)
    # - Terms stored as rows of an array; (i+1)^th column is the power of xi
    #   and 1st column is the coefficient

    # Default values
    disp_type = 1           # 0 means none, 1 means array, 2 means polynomial string
    default_mod_prime = 2

    # Test if prime when finite
    if (mod_prime != Inf) && (isprime(mod_prime) == false)
        println("Warning: Provided value for mod_prime is not a prime number.")
    end

    # Check that degree of all inputs is the same
    all_degrees = sum(poly_array[:, 2:end], dims = 2)
    if length(unique(all_degrees)) > 1
        println("Warning: Non-homogeneous input polynomial provided, multiple total degrees detected.")
    end

    # Store the power shift value
    if (mod_prime == 2) || (mod_prime == Inf)
        power_shift = 2
    else
        power_shift = mod_prime
    end

    # Print the input string
    if disp_type != 0
        println(" ")
        if mod_prime != Inf
            println("STEENROD MOD ", string(mod_prime), " TABLE:")
        else
            println("STEENROD (INTEGRAL) TABLE:")
        end
        println("Input polynomial:")
        print_polynomial(poly_array)
    end

    # Initialize the output
    all_steenrod_results = Array{Array{Float64, 2}, 1}(undef, length(degrees))
    
    # Run the loop for each input row
    n = size(poly_array, 2) - 1
    for row = 1:size(poly_array, 1)
        # Create the array of initial terms, each entry gives the terms of 
        # (xi + xi^mod_prime)^cn before multiplication (use 2 if mod_prime = Inf)
        initial_terms = Array{Array{Int64, 2}, 1}(undef, n)
        for i = 1:n
            comp_i = zeros(Int64(poly_array[row, i + 1] + 1), n + 1)
            for j = 0:Int64(poly_array[row, i + 1])
                comp_i[j + 1, i + 1] = j*(power_shift - 1) + poly_array[row, i + 1]
                comp_i[j + 1, 1] = binomial(Int64(poly_array[row, i + 1]), j)
            end
            initial_terms[i] = comp_i
        end

        # Multiply out the initial terms to get the result
        entire_result = zeros(Int64(prod(poly_array[row, 2:end] .+ 1)), n + 1)
        index = 1
        index_array = zeros(Int64, n)
        while index <= size(entire_result, 1)
            # Create the current term
            current_term = zeros(n + 1)
            for i = 1:n
                temp = initial_terms[i]
                used_initial_term = temp[index_array[i] + 1, :]
                if i == 1
                    current_term = used_initial_term
                else
                    current_term[2:n + 1] += used_initial_term[2:n + 1]
                    current_term[1] *= used_initial_term[1]
                end
            end
            entire_result[end - index + 1, :] = current_term
            entire_result[end - index + 1, 1] = entire_result[end - index + 1, 1]*poly_array[row, 1]        # multiply by constant in front
    
            # Create new index array
            index += 1
            index_array[n] += 1
            for i = n:-1:2
                if index_array[i] > poly_array[row, i + 1]
                    index_array[i] = 0
                    index_array[i - 1] = index_array[i - 1] + 1
                end
            end
        end

        # Extract only the terms of the proper degree, modulo mod_prime
        for i = 1:length(degrees)
            # Extract the results
            shift = (power_shift - 1)*degrees[i]
            steenrod_result = Array{Float64, 2}(undef, 0, n + 1)
            for j = 1:size(entire_result, 1)
                if mod_prime != Inf
                    if (sum(entire_result[j, 2:n + 1]) == sum(poly_array[row, 2:end]) + shift) && (mod(entire_result[j, 1], mod_prime) != 0)
                        new_steenrod_result = Array{Float64, 2}(undef, size(steenrod_result, 1) + 1, n + 1)
                        new_steenrod_result[1:end - 1, :] = steenrod_result
                        new_steenrod_result[end, :] = entire_result[j, :]
                        new_steenrod_result[end, 1] = mod(new_steenrod_result[end, 1], mod_prime)
                        steenrod_result = new_steenrod_result
                    end
                else
                    if (sum(entire_result[j, 2:n + 1]) == sum(poly_array[row, 2:end]) + shift) && (entire_result[j, 1] != 0)
                        new_steenrod_result = Array{Float64, 2}(undef, size(steenrod_result, 1) + 1, n + 1)
                        new_steenrod_result[1:end - 1, :] = steenrod_result
                        new_steenrod_result[end, :] = entire_result[j, :]
                        steenrod_result = new_steenrod_result
                    end
                end
            end
            
            # Store zero-array as steenrod result if empty
            if isempty(steenrod_result)
                steenrod_result = zeros(1, n + 1)
            end
        
            # Store the results
            if isassigned(all_steenrod_results, i)
                old_steenrod_result = all_steenrod_results[i]
                new_steenrod_result = Array{Float64, 2}(undef, size(old_steenrod_result, 1) + size(steenrod_result, 1), n + 1)
                new_steenrod_result[1:size(old_steenrod_result, 1), :] = old_steenrod_result
                new_steenrod_result[size(old_steenrod_result, 1) + 1:end, :] = steenrod_result
                all_steenrod_results[i] = new_steenrod_result
            else
                all_steenrod_results[i] = steenrod_result
            end
        end
    end

    # Add together duplicate powers
    for i = 1:length(degrees)
        steenrod_result = all_steenrod_results[i]
        j = 1
        while j <= size(steenrod_result, 1) - 1
            k = j + 1
            while k <= size(steenrod_result, 1)
                if steenrod_result[j, 2:end] == steenrod_result[k, 2:end]
                    steenrod_result[j, 1] += steenrod_result[k, 1]
                    if mod_prime != Inf
                        steenrod_result[j, 1] = mod(steenrod_result[j, 1], mod_prime)
                    end
                    steenrod_result = steenrod_result[1:end .!= k, :]
                else
                    k += 1
                end
            end
            j += 1
        end
        all_steenrod_results[i] = steenrod_result;
    end

    # Refilter by mod_prime if necessary
    if mod_prime != Inf
        for i = 1:length(degrees)
            steenrod_result = all_steenrod_results[i]
            j = 1
            while j <= size(steenrod_result, 1)
                if mod(steenrod_result[j, 1], mod_prime) == 0
                    steenrod_result = steenrod_result[1:end .!= j, :]
                else
                    j += 1
                end
            end
            all_steenrod_results[i] = steenrod_result
        end
    end

    # Fill in gaps in all_steenrod_results
    for i = 1:length(degrees)
        if isempty(all_steenrod_results[i])
            all_steenrod_results[i] = zeros(1, n + 1)
        end
    end

    # Display the results
    if disp_type != 0
        for i = 1:length(degrees)
            shift = degrees[i]
            steenrod_result = all_steenrod_results[i]
            println("Steenrod ", string(Int64(shift)), ":")
            if minimum(steenrod_result .== 0) == 1
                if disp_type == 1
                    println("     N/A")
                else
                    println("     0")
                end
                println(" ")
            else
                if disp_type == 1
                    for j = 1:size(steenrod_result, 1)
                        print("     ")
                        println(steenrod_result[j, :])
                    end
                    println(" ")
                else
                    print_polynomial(steenrod_result)
                end
            end
        end
    end

    # If only shift shift value wanted, convert output to an array (not an array of array)
    if length(degrees) == 1
        all_steenrod_results = all_steenrod_results[1]
    end

    return all_steenrod_results
end

function print_polynomial(poly_array)
    # - Prints the polynomial stored in poly_array
    # - Terms stored as rows of an array; (i+1)^th column is the power of xi
    #   and 1st column is the coefficient
    
    for i = 1:size(poly_array, 1)
        to_print = "     "
        to_print *= string(poly_array[i, 1])
        to_print *= "*"
        for j = 2:size(poly_array, 2)
            to_print *= "x"
            to_print *= string(j - 1)
            to_print *= "^"
            to_print *= string(Int64(poly_array[i, j]))
            if j < size(poly_array, 2)
                to_print *= "*"
            end
        end
        if i < size(poly_array, 1)
            to_print *= " +"
        end
        println(to_print)
    end
    println(" ")
    
end

function isprime(n)
    # Tests if a number is prime

    if n < 2
        return false
    end
    for i = 2:Int(floor(sqrt(n)))
        if n % i == 0
            return false
        end
    end
    return true
end

# Main working polynomial (first column is the coeffiecnt, rest of powers)
#steenrod([1 4 2 1; 1 4 1 2; 1 2 4 1; 1 2 1 4; 1 1 4 2; 1 1 2 4])
#steenrod([2 6], mod_prime = 3)
#steenrod([2 3 3], mod_prime = 3)
#steenrod([1 5], mod_prime = 5)

#steenrod([1 1 4 2; 1 1 2 4])
#steenrod([1 4 2 1; 1 4 1 2])
#steenrod([1 2 4 1; 1 2 1 4])

steenrod([1 6])
steenrod([1 2 4])
steenrod([1 2 2 2])

# End the code
println("Press enter key to close...")
readline()
