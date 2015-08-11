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

        public Type MetricType { get; private set; }

        [JsonProperty("metricType")]
        public string MetricValueType => MetricType.Name == "Single" ? "float" : MetricType.Name;

        public ReduceEnum ReduceType { get; private set; }

        [JsonProperty("reduce")]
        public string Reduce => ReduceType.ToString();

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
            MetricType = metricType;
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
