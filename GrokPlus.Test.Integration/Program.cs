using System;
using System.Threading.Tasks;
using NetMQ;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace GrokPlus.Test.Integration
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            var subscriberPort = args[0];
            var publisherPort = args[1];

            //Console.WriteLine("Starting subscriber...");
            //Task.Run(() => Subscriber(subscriberPort)).ConfigureAwait(false);
            Console.WriteLine("Starting publisher...");
            Task.Run(() => Publisher(publisherPort)).ConfigureAwait(false);

            Console.WriteLine("Starting indefinite loop...");
            while (true)
            {
            }
        }

        private static void Subscriber(string port)
        {
            string topic = "TopicA"; // one of "TopicA" or "TopicB"

            using (var context = NetMQContext.Create())
            using (var subSocket = context.CreateSubscriberSocket())
            {
                subSocket.Options.ReceiveHighWatermark = 1000;
                subSocket.Connect($"tcp://127.0.0.1:{port}");
                subSocket.Subscribe(topic);
                Console.WriteLine("$Subscriber socket connecting to port {port}...");

                while (true)
                {
                    string messageTopicReceived = subSocket.ReceiveString();
                    Console.WriteLine("Receiving message...");
                    string messageReceived = subSocket.ReceiveString();
                    Console.WriteLine(messageReceived);
                }
            }
        }

        private static void Publisher(string port)
        {
            using (var context = NetMQContext.Create())
            using (var pubSocket = context.CreatePublisherSocket())
            {
                Console.WriteLine($"Publisher socket binding to port {port}...");
                pubSocket.Options.SendHighWatermark = 1000;
                pubSocket.Bind($"tcp://127.0.0.1:{port}");

                var rand = new Random(50);
                var personId = Guid.NewGuid();

                System.Threading.Thread.Sleep(1000);
                var metric = CreateMetric("mood", personId, 0, 10);
                pubSocket.SendMore("MetricCreated").Send(metric.ToString().Replace("\n", "").Replace("\r", ""));

                System.Threading.Thread.Sleep(1000);
                metric = CreateMetric("sleep", personId, 0, 5);
                pubSocket.SendMore("MetricCreated").Send(metric.ToString().Replace("\n", "").Replace("\r", ""));

                while (true)
                {
                    System.Threading.Thread.Sleep(1000);
                    var randomizedTopic = rand.NextDouble();

                    JObject msg = new JObject();

                    msg = randomizedTopic > 0.5 ? CreateReading("mood", personId, 0, 10) : CreateReading("sleep", personId, 0, 5);

                    Console.WriteLine("Sending message : {0}", msg.ToString());
                    pubSocket.SendMore("EncodingCreated").Send(msg.ToString().Replace("\n", "").Replace("\r", ""));
                }
            }
        }

        private static JObject CreateMetric(string metric, Guid personId, decimal minValue, decimal maxValue)
        {
            return new JObject
            {
                [nameof(personId)] = personId.ToString(),
                [nameof(metric)] = metric,
                [nameof(minValue)] = minValue,
                [nameof(maxValue)] = maxValue
            };
        }

        private static JObject CreateReading(string metric, Guid personId, decimal minValue, decimal maxValue)
        {
            return new JObject
            {
                [nameof(personId)] = personId.ToString(),
                [nameof(metric)] = metric,
                ["value"] = RandomNumberBetween(minValue, maxValue),
                ["timestamp"] = System.DateTime.Now
            };
        }

        private static readonly Random random = new Random();

        private static decimal RandomNumberBetween(decimal minValue, decimal maxValue)
        {
            decimal next = Convert.ToDecimal(random.NextDouble());

            return minValue + ((decimal)next * (maxValue - minValue));
        }
    }
}
