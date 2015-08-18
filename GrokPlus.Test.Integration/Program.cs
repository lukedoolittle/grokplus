using System;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using GrokPlus.Test.Integration.Encodings;
using Microsoft.VisualBasic.FileIO;
using NetMQ;
using NetMQ.Sockets;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using Pacman.Domain.Events;
using Pacman.Domain.Write.Encodings;
using Pacman.Framework.Serialization;

namespace GrokPlus.Test.Integration
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            //var subscriberPort = 6001;
            var publisherPort = 6000;
            //var address = "127.0.0.1";
            var address = "52.21.106.130";

            JsonConvert.DefaultSettings = () => new JsonSerializerSettings
            {
                MissingMemberHandling = MissingMemberHandling.Ignore,
                DefaultValueHandling = DefaultValueHandling.Ignore,
                ContractResolver = new PrivateMembersContractResolver(),
                TypeNameHandling = TypeNameHandling.All
            };

            //Console.WriteLine("Starting subscriber...");
            //Task.Run(() => Subscriber(subscriberPort)).ConfigureAwait(false);

            Console.WriteLine("Starting publisher...");
            Task.Run(() => Publisher(address, publisherPort.ToString())).ConfigureAwait(false);

            Console.WriteLine("Starting indefinite loop...");
            while (true)
            {
            }
        }

        //private static void Subscriber(string port)
        //{
        //    string topic = "TopicA"; // one of "TopicA" or "TopicB"

        //    using (var context = NetMQContext.Create())
        //    using (var subSocket = context.CreateSubscriberSocket())
        //    {
        //        subSocket.Options.ReceiveHighWatermark = 1000;
        //        subSocket.Connect($"tcp://127.0.0.1:{port}");
        //        subSocket.Subscribe(topic);
        //        Console.WriteLine("$Subscriber socket connecting to port {port}...");

        //        while (true)
        //        {
        //            string messageTopicReceived = subSocket.ReceiveString();
        //            Console.WriteLine("Receiving message...");
        //            string messageReceived = subSocket.ReceiveString();
        //            Console.WriteLine(messageReceived);
        //        }
        //    }
        //}

        private static void Publisher(string address, string port)
        {
            using (var context = NetMQContext.Create())
            using (var pubSocket = context.CreatePublisherSocket())
            {
                Console.WriteLine($"Publisher socket connecting to port {port}...");
                pubSocket.Options.SendHighWatermark = 1000;
                pubSocket.Connect($"tcp://{address}:{port}");

                var personId = Guid.NewGuid();

                Thread.Sleep(1000);

                Console.WriteLine("Create metric Metric1");
                CreateMetric<Metric1>(personId, pubSocket);
                Console.WriteLine("Create metric Metric2");
                CreateMetric<Metric2>(personId, pubSocket);
                Console.WriteLine("Create metric Metric3");
                CreateMetric<Metric3>(personId, pubSocket);
                Console.WriteLine("Create metric Metric4");
                CreateMetric<Metric4>(personId, pubSocket);
                Console.WriteLine("Create metric Metric5");
                CreateMetric<Metric5>(personId, pubSocket);

                Console.WriteLine("Getting samples from csv...");
                using (TextFieldParser parser = new TextFieldParser(@"test1.csv"))
                {
                    parser.TextFieldType = FieldType.Delimited;
                    parser.SetDelimiters(",");

                    //The first three lines don't contain metric readings
                    //so throw them away
                    Console.WriteLine("Throwing away opening lines...");
                    parser.ReadFields();
                    parser.ReadFields();
                    parser.ReadFields();

                    while (!parser.EndOfData)
                    {
                        Console.WriteLine("Got a row");
                        //Processing row
                        string[] fields = parser.ReadFields();

                        if (fields == null ||
                            !fields.Any())
                        {
                            throw new Exception();
                        }

                        string timestamp = fields[0];

                        Console.WriteLine("Creating 5 encodings");
                        CreateEncoding<Metric1>(fields[1], timestamp, personId, pubSocket);
                        CreateEncoding<Metric2>(fields[2], timestamp, personId, pubSocket);
                        CreateEncoding<Metric3>(fields[3], timestamp, personId, pubSocket);
                        CreateEncoding<Metric4>(fields[4], timestamp, personId, pubSocket);
                        CreateEncoding<Metric5>(fields[5], timestamp, personId, pubSocket);
                    }
                }
            }
        }

        private static void CreateMetric<TEncoding>(
            Guid personId, 
            PublisherSocket socket)
            where TEncoding : Encoding
        {
            var metric = new MetricCreated<TEncoding>(
                -1, 
                1, 
                typeof(float), 
                ReduceEnum.Average, 
                Guid.NewGuid(), 
                personId);
            var json = metric.AsJson(false).Replace("\n", "").Replace("\r", "");
            socket.SendMore(metric.GetType().Name).Send(json);
        }

        private static void CreateEncoding<TEncoding>(
            string value,
            string timestamp,
            Guid personId,
            PublisherSocket socket)
            where TEncoding : Encoding
        {
            var encoding = new EncodingCreated<TEncoding>(
                JValue.CreateString(value),
                timestamp,
                Guid.NewGuid(),
                personId);
            var json = encoding.AsJson(false).Replace("\n", "").Replace("\r", "");
            socket.SendMore(encoding.GetType().Name).Send(json);
        }
    }
}
