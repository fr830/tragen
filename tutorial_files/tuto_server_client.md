    
Once the data model has been defined and an *UaDataStruct* has been created, we can create an opcua Tragen server, load the data into its address space and start one or more clients.    
    
# Tragen Server:    
    
## How to start it?    
We start by chosing an address (port, uri) and optionally a name for the server, then we instantiate the ServerTragen class.      
```python    
>>> srv_url="opc.tcp://0.0.0.0:4840/tragen0/server0/"    
>>> srv_name="myServer"    
>>> server = ServerTragen(srv_url, name=srv_name)     
```    
Now we have an instance of ServerTragen, but it has not yet been started and data hasn't been loaded yet.    
To do so, we just make a call to the init method and pass the previously defined *UaDataStruct* object.    
```python    
>>> server.init(data_nodes=ua_graph)    
```    
The server should now be running and be able to receive client connections.    
    
## What happens inside the *init()* method?    
    
We will look at the code the function.    
```python    
  def init(self, data_nodes=None, by_xml=False):
      """
      Set an endpoint, define accepted security policies, populates the adress space,
      create the notification events (to which clients can subscribe), then starts the
      server.

      :type data_nodes:  UaDataStruct()
      """
      self.set_endpoint(self.uri)
      self.set_server_name(self.name)

      self.set_security_policy([
              ua.SecurityPolicyType.NoSecurity,
              ua.SecurityPolicyType.Basic128Rsa15_SignAndEncrypt,
              ua.SecurityPolicyType.Basic128Rsa15_Sign,
              ua.SecurityPolicyType.Basic256_SignAndEncrypt,
              ua.SecurityPolicyType.Basic256_Sign])

      #self.load_certificate("server_cert.pem")
      #self.load_private_key("server_private_key.pem")

      # populating the address space
      self.populate_ns(data_nodes, by_xml)
      # creating notification events (if there's any, for clients to subscribe to)
      self.create_notifying_events(self.get_root_node(), self.get_objects_node(), data_nodes._graph)
      
      if self.independant:
          # Create an updater thread for every updatable variable then start it
          self.var_updaters = self.set_updaters(data_nodes._graph)
          for updater in self.var_updaters:
              updater.start()
          # Create  notifier thread for every monitored variable then start it
          self.notifiers = self.set_notifiers()
          for notifier in self.notifiers:
              notifier.start()

      self.start()

```    
    
As explained in the Docstring, this method sets and endpoint with the specified URL.    
Then, it specifies the accepted security policies that a client can choose to communicate with the server on the Secure Channel. By default, the cient will select *NoSecurity*, so to enforce authentication or encryption, the *ua.SecurityPolicyType.NoSecurity* must be removed from the set.    
Afterwards, it will populate the address space with data and change writing permissions for writable nodes.    
The next part is about creating notification events for variables that are supposed to be updated regularly. As specified in the *UaDataStruct*, this variables have a "safe" range of values, if their value gets outside this range, a notification is sent to the subscribed clients.    
If the ServerTragen is launched outside a Tragen context, it will create an updater thread for every updatable variable, and create notifier threads that will actually trigger the notification events created before.    
Finally, when everything is set, the server is started.    
  
  
# Tragen Client:  
  
## How to start it?  
We follow the exact same steps as for the server.  
```python  
>>> srv_url="opc.tcp://10.210.16.12:4840/tragen0/server0/"  
>>> client = ClientTragen(srv_url)  
>>> client.init(ua_data_struct=ua_graph)  
```  
The graph must be shared between the server and the client.  
The client has to either build the same graph locally, or find a way to get a copy from the server.  
  
  
## What happens inside the *init()* method?    
    
We will look at the code the function.    
```python    
  def init(self, ua_data_struct=None):
      """
      Connect to the server, and initialize subscriptions if the server's data nodes are provided.

      :type ua_data_struct:   UaDataStruct()
      """
      # Security policy (Uncomment to enable)
      #self.set_security(security_policies.SecurityPolicyBasic128Rsa15, "client_cert.pem", "client_private_key.pem", server_certificate_path="server_cert.pem")
      self.connect()
      self.connected = True
      self.load_type_definitions()
      if ua_data_struct is not None:
          self.initialize_subs(ua_data_struct._graph)
      if self.independant:
          writables, readables = self.setup_rw(ua_data_struct._graph)
          self.set_client_agents(readables, writables, ua_data_struct._graph)
          self.writer.start()
          self.reader.start()
```  
  
After establishing a connection with the server, it explores the graph and subscribes to every node that is updatable.  
It also constructs a list of all the writable and readable variables and use it to create a writer thread (that will randomly modify writable variables) and a reader thread (that will send random read requests to the server).  
  
  
