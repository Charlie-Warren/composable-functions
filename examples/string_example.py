import composablefunctions as cf
from my_string_lib_example import make_uppercase, foo

composed = cf.ComposedFunction()

input_string="hello"

# Add "foo", which doesn't do much except describe itself
composed.add_function(foo, "world", "!", extraword="world", extranumber=5)
# Print the output when applied to "hello"
print(composed.apply(input_string))

# Now add the make_uppercase function and see the new result when applied to "hello"
composed.add_function(make_uppercase)
print(composed.apply(input_string))
