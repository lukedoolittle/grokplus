using System;
using Newtonsoft.Json;

namespace Pacman.Domain.Events
{
    public class Event
    {
        //TOD: refactor this so that these setters are private
        public Guid Id { get; set; }

        [JsonProperty("personId")]
        public Guid AggregateId { get; set; }

        public int Version { get; set; }
    }
}
