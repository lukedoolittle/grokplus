using System;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using Pacman.Domain.Write.Encodings;

namespace Pacman.Domain.Events
{
    public class EncodingCreated<TEncoding> : Event
        where TEncoding : Encoding
    {
        [JsonProperty("value")]
        public JValue Payload { get; private set; }

        [JsonProperty("timestamp")]
        public DateTimeOffset Timestamp { get; private set; }

        [JsonProperty("metric")]
        public string Metric => typeof (TEncoding).Name;

        public EncodingCreated(
            JValue payload,
            DateTimeOffset timestamp,
            Guid id,
            Guid aggregateId)
        {
            Payload = payload;
            Timestamp = timestamp;
            Id = id;
            AggregateId = aggregateId;
        }
    }
}
