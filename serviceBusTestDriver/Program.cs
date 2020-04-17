using System;
using System.Diagnostics;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Azure.ServiceBus;
using Microsoft.Azure.ServiceBus.Management;

namespace serviceBusTestDriver
{
    class Program
    {
        static string ServiceBusMgmtConnectionString;
        static string ServiceBusConnectionString;
        static string QueueName;
        static IQueueClient queueClient;
        static Stopwatch stopWatch;

        public static async Task Main(string[] args)
        {
            ServiceBusMgmtConnectionString = Environment.GetEnvironmentVariable("ServiceBusMgmtConnectionString", EnvironmentVariableTarget.Process).ToString();
            ServiceBusConnectionString = Environment.GetEnvironmentVariable("ServiceBusConnectionString", EnvironmentVariableTarget.Process).ToString();
            QueueName = Environment.GetEnvironmentVariable("QueueName", EnvironmentVariableTarget.Process).ToString();
            int numberOfMessages = -1;

            var managementClient = new ManagementClient(ServiceBusMgmtConnectionString);

            string sRead = "";
            Console.WriteLine("======================================================");
            Console.WriteLine("Press nummber of messages to send or Q to qutt");
            Console.WriteLine("======================================================");
            queueClient = new QueueClient(ServiceBusConnectionString, QueueName);
            sRead = Console.ReadLine();
            Console.WriteLine("Starting process at {0}", DateTime.Now.ToShortTimeString());
            Console.WriteLine("======================================================");
            Console.WriteLine("Sending messages to queue...");

            stopWatch = Stopwatch.StartNew();
            if (Int32.TryParse(sRead, out numberOfMessages))
                // Send messages.
                await SendMessagesAsync(numberOfMessages);

            Console.WriteLine("======================================================");
            Console.WriteLine("Waiting for queue to drain...");
            long messagesInQueueCount = -1;
            do
            {
                var runtimeInfo = await managementClient.GetQueueRuntimeInfoAsync(QueueName);
                messagesInQueueCount = runtimeInfo.MessageCountDetails.ActiveMessageCount;
                if (messagesInQueueCount != 0)
                    Thread.Sleep(500);
            } while (messagesInQueueCount > 0);
            stopWatch.Stop();
            Console.WriteLine("======================================================");
            Console.WriteLine("Ending process at {0}", DateTime.Now.ToShortTimeString());
            Console.WriteLine("Time to drain queue in seconds: " + stopWatch.ElapsedMilliseconds / 1000);
            Console.WriteLine("======================================================");
            await queueClient.CloseAsync();
        }
        static async Task SendMessagesAsync(int numberOfMessagesToSend)
        {
            try
            {
                for (var i = 0; i < numberOfMessagesToSend; i++)
                {
                    // Create a new message to send to the queue.
                    string messageBody = "{\"name\":\"100540032.pdf\"}";
                    var message = new Message(Encoding.UTF8.GetBytes(messageBody));

                    // Write the body of the message to the console.
                    Console.WriteLine($"Sending message: {messageBody}");

                    // Send the message to the queue.
                    await queueClient.SendAsync(message);
                }
            }
            catch (Exception exception)
            {
                Console.WriteLine($"{DateTime.Now} :: Exception: {exception.Message}");
            }
        }
    }
}
