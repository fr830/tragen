from opcua import ua
from tragen import *




def main():

    # The next part is duplicated code from 'example.py'

    #################################################
    # Defining OPC UA server's data graph
    #################################################

    # We can instantiate an empty graph or initialize it with some elements (line below)
    ua_graph = UaDataStruct(folder="example_folder_1", ua_object="object_1", ua_variables=[("var_11",02),("var_12",12.5)], ua_properties=[("property_example","running")])
    
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
    
    # The 'is_writable' attribute decides wether it the variable/property's value can be written/modified by clients
    ua_graph.find_variable("var_21")[0].is_writable = True
    # We select the first element returned by 'find_objetc' (In this example the list contains one entry)
    # We select its content (which is dictionnary) and take the first property (there's only on in this example '1st_property_of_object3')
    # We set it to be writable by clients
    ua_graph.find_object("object_3")[0][1]["properties"][0].is_writable = True
    
    # 'is_irreg_ud' : variable's value is updated every now and then. (By default, the clients subscribed to it, will get notified about this change)
    # 'is_reg_ud' : variable's value is updated with fixed intervals. (By default, the clients subscribed to it, will get notified whenever its value goes below or above a threshold)
    ua_graph.find_variable("var_21")[0].is_irreg_ud = True
    ua_graph.find_variable("var_12")[0].is_reg_ud = True
    

    #################################################
    # Starting the server:
    #################################################
    srv_url="opc.tcp://0.0.0.0:4840/tragen0/server0/"
    srv_name="opc-server"
    server = ServerTragen(srv_uri=srv_url, name=srv_name)
    server.init(data_nodes=ua_graph)





if __name__ == '__main__':
    main()



