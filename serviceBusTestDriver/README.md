Make sure to add this to your csproj.user file:

    <EnvironmentVariables>
      <Variable name="ServiceBusMgmtConnectionString" value=<queue mgmt conn string" xmlns="" />
      <Variable name="ServiceBusConnectionString" value="queue conn string" xmlns="" />
      <Variable name="QueueName" value="pythonfunctiontesting" xmlns="" />
    </EnvironmentVariables>