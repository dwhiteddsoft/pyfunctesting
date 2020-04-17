# Service Bus Test Driver

This program will drive messages into the configured service bus and then wait for the queue to drain to zero. It will time from the first message sent until the queue is drained. This makes the assumption the function picks up the first message when it arrives. 

## Make Sure To Do

Make sure to add this to your csproj.user file:

    <EnvironmentVariables>
      <Variable name="ServiceBusMgmtConnectionString" value=<queue mgmt conn string" xmlns="" />
      <Variable name="ServiceBusConnectionString" value="queue conn string" xmlns="" />
      <Variable name="QueueName" value="pythonfunctiontesting" xmlns="" />
    </EnvironmentVariables>