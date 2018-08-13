  
The *UaDataStruct* is one of the main components of Tragen. An instance of this class defines the data model that will be stored in the server (nodes, variables, objects, ..) and also defines the logic of how these nodes will be used by the clients and the server alike.    
All the elements of the generated graph (folders, variables, ..) are represented by nodes. They are instances of different objects, all inheriting the *TragenNodeStruct* class structure.    
Their attributes describe their behavior (i.e how the server/clients will modify them) and the read permissions.    
  
# *UaDataStruct* graph:  
  
This graph of TragenNodes and their dependencies is built using python dictionaries. It was designed this way to make for an easy recursive functions that explore it.    
    
The root (i.e the main dictionary, *UaDataStruct.\_graph*) contains four elements, their keys are 'folders', 'objects', 'variables' and 'properties'.    
root['variables'] and root['properties'] are lists of TragenVariable and TragenProperty instances respectively.    
root['objects'] is a dictionary of ua\_objects where the keys are TragenObjects and their values are dictionaries. These latter contain two elements that are referenced with the following keys: 'variables', 'properties'. (These are two lists of TragenVariable/TragenProperty instances).    
Example:    
```python
root['objects']	= {	TragenObject: {'variables': [TragenVariable, ...], 'properties': [TragenProperty, ...]}    
			...    
		  }    
```
  
root['folders'] is a dictionary where the keys are TragenFolders and their values are dictionaries which format is similar to that of root.  
Example:  
```python
root['folders'] = {	TragenFolder:	{	variables': 	[TragenVariable, ...],   
				    		properties': 	[TragenProperty, ...],  
				    		objects':	{	TragenObject: {'variables': [TragenVariable, ...], 'properties': [TragenProperty, ...]}   
                                            				...  
                                          			},  
				    		folders': 	{ TragenFolder: {'folders': ..., 'objects': ..., 'variables': ..., 'properties': ...}}  
                                  	},  
                    	....  
		  }  
```
  
  
# Getting Started: Defining OPC UA server's data graph.  
  
## Creating a graph of folders, objects, variables and properties.  
  
We can instantiate an empty *UaDataStruct* graph or initialize it with some elements (code snippet below).  
All the parameters are optional, we can add nodes after instantation.  
For the class *\_\_init\_\_()* and all of the other methods of adding nodes to the graph, the folder and object parameters (folder, ua\_object) are strings representing their name.  
The variables and properties parameters take a list of tuples representing the name and the value of each variable/property.  
```python  
>>> from opcua import ua  
>>> from tragen import *  
>>> ua_graph = UaDataStruct(folder="example_folder_1", ua_object="object_1", ua_variables=[("var_11",02),("var_12",12.5)], ua_properties=[("property_example","running")])  
```  
We can use the method *show()* to print the graph.      
```python  
>>> ua_graph.show()  
[]] example_folder_1 (ns=1)  
 |__[+] object_1 (ns=1)  
 |   |__[*] Variable: (var_11, 2) (ns=1)  
 |   |__[*] Variable: (var_12, 12.5) (ns=1)  
 |   |__[*] Property: (property_example, running) (ns=1)  
>>>  
```  
  
Defining an additional folder named 'example\_folder\_2'.  
Let's add two objects to it using two different approaches.  
```python  
>>> folder2 = ua_graph.add_folder("example_folder_2")   
```  
We've kept our new folder's in a variable 'folder2' for later use but it's not necessary.  
As shown below, to add a new object, we can either use the folder's name as a reference, or its node in the graph.  
(Objects that are not added to any folder will be placed in the objects folder, right under the root node).  
```python  
>>> # Adding and object to 'example_folder_2' using its corresponding folder node  
>>> ua_graph.add_object("object_2", folder_node=folder2, ua_properties=[("this_is_a_property","stopped")], ua_variables=[("var_21",0),("var_22", 1), ("var_23", 2)])  
>>>   
>>> # Adding a second object to 'example_folder_2' referring to it by its name  
>>> ua_graph.add_object("object_3", folder_name="example_folder_2", ua_properties=[("first_property_of_object3","random")])  
```  
Your graph should look like this:  
```python  
>>> ua_graph.show()  
[]] example_folder_2 (ns=0)  
 |__[+] object_2 (ns=0)  
 |   |__[*] Variable: (var_21, 0) (ns=0)  
 |   |__[*] Variable: (var_22, 1) (ns=0)  
 |   |__[*] Variable: (var_23, 2) (ns=0)  
 |   |__[*] Property: (this_is_a_property, stopped) (ns=0)  
 |__[+] object_3 (ns=0)  
 |   |__[*] Property: (first_property_of_object3, random) (ns=0)  
[]] example_folder_1 (ns=1)  
 |__[+] object_1 (ns=1)  
 |   |__[*] Variable: (var_11, 2) (ns=1)  
 |   |__[*] Variable: (var_12, 12.5) (ns=1)  
 |   |__[*] Property: (property_example, running) (ns=1)  
```  
Same thing for adding subfolders, we can either refer to their parent folder by its name or its node.  
Unless respecting a folder naming convention whereby all names are distinct, nodes are generally preferred over names.  
```python   
>>> # Adding a subflder to 'example_folder_1'  
>>> ua_graph.add_folder("subfolder_3", parent_name="example_folder_1")  
>>> ua_graph.add_folder("empty_4_added_using_its_parent_node", parent_node=folder2)  
```  
  
So far, we have added objects and their attributes at the same time.  
Let's add an empty object and **then** add elements to it.  
```python  
>>> # Adding an object then adding a property to it as an attribute  
>>> ua_graph.add_object("object_4")  
>>> ua_graph.add_property("BestProperty","ValueofBestProperty", par_name="object_4")  
```  
Same thing for variables, we use 'add\_variable' with the name and the value of the variable passed as parameters, then one of the  
following parameter 'par\_name' or 'par\_node' (parent name or parent node).  
  
```python  
>>> # The following must be self-explanatory.  
>>> ua_graph.add_folder("subfolder_4", parent_name="example_folder_1")  
>>> ua_graph.add_object("myobject_5", folder_name="subfolder_4", ua_properties=[("AnotherProperty", "random_value")])  
>>> ua_graph.show()  
```  
      
## Logic, permissions, and other methods...  
  
Setting up some configuration before initialization of Tragen clients and server.  
Defining some properties of the elements in the graph.  
Folders, objects, variables and properties within the graph have some attributes that could be customized.  
NB: the graph is just a description of the server's data. Changes on the server will not take effect until *init()* is called.  
      
### *Find* methods:  
  
* if find\_[variable/property] is called with only a name it will return a list of variable/property nodes with this name.  
* if find\_[folder/object] is called with only a name it will return a list of tuples [(folder/object, content)] where folders/objects is the corresponding TragenNode and content is graph (dictionnary)  
      
### Write permission:  
The 'is\_writable' attribute decides wether the variable/property's value can be written/modified by clients or not.  
This descriptor is used by the server to give writing rights to clients for the corresponding node.   
It is also used by the *init()* method of the client to know which nodes should be modified by the Writer thread.  
```python  
>>> ua_graph.find_variable("var_21")[0].is_writable = True  
```  
  
To make things clear, let's break apart the next example into steps to understand what happens.  
```python  
>>> ua_graph.find_object("object_3")[0][1]["properties"][0].is_writable = True  
```  
First, we select the first element returned by 'find\_object' (In this example the list contains only one entry).    
Then, we select content (1, second element of the returned tuple), which is a dictionnary of variables and properties.  
```python  
>>> object_3, object_3_content = ua_graph.find_object("object_3")[0]
or 
>>> _, object_3_content = ua_graph.find_object("object_3")[0]
or 
>>> object_3 = ua_graph.find_object("object_3")[0][1]
```  
We then take the first property (there's only oen in this example 'first\_property\_of\_object3').  
```python  
>>> first_property = object_3_content.["properties"][0]
```  
Finally, we set it to be writable by clients.  
```python  
>>> first_property.is_writable = True  
```  

### Non-static variables:  
By default variables are static, if not (i.e is\_reg\_ud or is\_irreg\_id is true) then the server will make sure to keep updating its value  
'is\_irreg\_ud' : variable's value is updated every now and then. (By default, the clients subscribed to it, will get notified about this change)  
'is\_reg\_ud' : variable's value is updated with fixed intervals. (By default, the clients subscribed to it, will get notified whenever its value goes below or above a threshold)  
```python  
>>> ua_graph.find_variable("var_21")[0].is_irreg_ud = True  
>>> ua_graph.find_variable("var_12")[0].is_reg_ud = True  
```  
