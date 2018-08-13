from opcua import ua
from tragen import *
from IPython import embed




def main():

    # Defining OPC UA server's data graph
    # We can instantiate an empty graph or initialize it with some elements (line below)
    ua_graph = UaDataStruct(folder="example_folder_1", ua_object="object_1", ua_variables=[("var_11",02),("var_12",12.5)], ua_properties=[("property_example","running")])
    embed()
    
    # Defining an additional folder names 'example_folder_2'
    folder2 = ua_graph.add_folder("example_folder_2")
    
    # Adding and object to 'example_folder_2' using its coreesponding folder node
    ua_graph.add_object("object_2", folder_node=folder2, ua_properties=[("this_is_a_property","stopped")], ua_variables=[("var_21",0),("var_22", 1), ("var_23", 2)])
    
    # Adding a second object to 'example_folder_2' referring to it by its name
    ua_graph.add_object("object_3", folder_name="example_folder_2", ua_properties=[("1st_property_of_object3","random")])
    
    # Adding a subflder to 'example_folder_1'
    ua_graph.add_folder("subfolder_3", parent_name="example_folder_1")
    
    # Adding an object then adding a property to it as an attribute
    ua_graph.add_object("object_4")
    ua_graph.add_property("BestProperty","ValueofBestProperty", par_name="object_4")
    
    # Self-explanatory
    ua_graph.add_folder("subfolder_4", parent_name="example_folder_1")
    ua_graph.add_object("myobject_5", folder_name="subfolder_4", ua_properties=[("AnotherProperty", "random_value")])
    
    # Create a Tragen context with 3 cients
    # The server will be assigned a default url
    ctx = Tragen(nb_client=3)
    
    # Setting up some configuration before initialization
    # Defining some properties of the elements in the graph
    # Folders, objects, variables and properties within the graph have some attributes that could be customized
    # NB: the graph is just a description of the server's data. Changes will not take effect until init() is called
    
    # if find_[variable/property] is called wit only a name it will return a list of variables/properties with this name
    # if find_[folder/object] is called wit only a name it will return a list of (folders/objects, content) where folders/objects bear this name and content is graph (dictionnary)
    
    # The 'is_writable' attribute decides wether it the variable/property's value can be written/modified by clients
    ua_graph.find_variable("var_21")[0].is_writable = True
    
    # What happens in the line below?
    # We select the first element returned by 'find_objetc' (In this example the list contains one entry)
    # We select its content (which is dictionnary) and take the first property (there's only on in this example '1st_property_of_object3')
    # We set it to be writable by clients
    ua_graph.find_object("object_3")[0][1]["properties"][0].is_writable = True
    
    # By default variables are static, if not (i.e is_reg_ud or is_irreg_id is true) then the server will make sure to keep updating its value
    # 'is_irreg_ud' : variable's value is updated every now and then. (By default, the clients subscribed to it, will get notified about this change)
    # 'is_reg_ud' : variable's value is updated with fixed intervals. (By default, the clients subscribed to it, will get notified whenever its value goes below or above a threshold)
    ua_graph.find_variable("var_21")[0].is_irreg_ud = True
    ua_graph.find_variable("var_12")[0].is_reg_ud = True
    
    
    # We initialize the tragen context
    # The server's address space will be populated with data from the 'UaDataStruct' graph, variable updates and events triggerers will be created accordingly
    # The clients will be connected to the server endpoint and susbscribe to nodes with varying/changing values
    # Random variable writer and reader are created for each client
    ctx.init(ua_srv_data=ua_graph)
    
    c1r = ctx.clients[1].get_root_node()
    # Adding a client
    ctx.add_client(ctx.srv_url)

    # Use the method show() to visualize the graph.
    #ua_graph.show()
         
    embed()


if __name__ == '__main__':
    main()



