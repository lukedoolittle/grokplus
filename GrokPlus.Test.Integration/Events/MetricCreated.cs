using System;
using Newtonsoft.Json;
using Pacman.Domain.Write.Encodings;

namespace Pacman.Domain.Events
{
    public class MetricCreated<TEncoding> : Event
        where TEncoding : Encoding
    {
        [JsonProperty("metric")]
        public string Metric => typeof(TEncoding).Name;

        [JsonProperty("minValue")]
        public decimal MinimumValue { get; private set; }

        [JsonProperty("maxValue")]
        public decimal MaximumValue { get; private set; }

        [JsonProperty("metricType")]
        public string MetricValueType { get; private set; }

        [JsonProperty("reduce")]
        public ReduceEnum ReduceType { get; private set; }

        public MetricCreated(
            decimal minimumValue,
            decimal maximumValue,
            Type metricType,
            ReduceEnum reduce,
            Guid id,
            Guid aggregateId)
        {
            MinimumValue = minimumValue;
            MaximumValue = maximumValue;
            MetricValueType = metricType.Name;
            ReduceType = reduce;
            Id = id;
            AggregateId = aggregateId;
        }
    }

    public enum ReduceEnum
    {
        Sum,
        Average
    }
}
