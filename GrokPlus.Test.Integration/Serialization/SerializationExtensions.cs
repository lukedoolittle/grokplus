using System;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.Linq;
using System.Reflection;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace Pacman.Framework.Serialization
{
    public static class SerializationExtensions
    {
        public static string AsJson(
            this object source, 
            bool withType = true)
        {
            return Serialize(source, withType);
        }

        private static string Serialize(
            object entity, 
            bool withType)
        {
            return JsonConvert.SerializeObject(
                entity, 
                GetSerializerSettings(withType));
        }

        public static TEntity AsEntity<TEntity>(
            this string source, 
            bool withType = true)
        {
            return Deserialize<TEntity>(source, withType);
        }

        public static TEntity AsEntity<TEntity>(
            this NameValueCollection source,
            bool withType = true)
        {
            var dictionary = source.Cast<string>()
                .ToDictionary(p => p, p => (object)source[p]);

            if (withType)
            {
                Type rootType = typeof(TEntity);
                var typedDictionary = new Dictionary<string, object>
                {
                    {"$type", $"{rootType.FullName}, {rootType.Assembly.GetName().Name}"}
                };
                foreach (var item in dictionary)
                {
                    typedDictionary.Add(item.Key, item.Value);
                }
                dictionary = typedDictionary;
            }

            return dictionary.AsEntity<TEntity>(true);
        }

        public static TEntity AsEntity<TEntity>(
            this IDictionary<string, object> source,
            bool withType = false)
        {
            string json = Serialize(source, false);
            return Deserialize<TEntity>(json, true);
        }

        private static TEntity Deserialize<TEntity>(
            string json, 
            bool withType)
        {
            if (string.IsNullOrEmpty(json))
            {
                return default(TEntity);
            }

            var result = (TEntity)JsonConvert.DeserializeObject(
                json, 
                null,
                GetSerializerSettings(withType));

            return result;
        }

        public static IDictionary<string, object> AsDictionary(
            this object source,
            BindingFlags bindingAttributes =
            BindingFlags.Public | 
            BindingFlags.Instance,
            bool withType = true)
        {
            IDictionary<string, JToken> jsonDictionary = JObject.FromObject(source);
            return jsonDictionary.ToDictionary(a => a.Key, a => (object) a.Value);
        }

        private static JsonSerializerSettings GetSerializerSettings(bool withType)
        {
            var serializerSettings = JsonConvert.DefaultSettings();

            if (!withType)
            {
                serializerSettings.TypeNameHandling = TypeNameHandling.None;
            }

            return serializerSettings;
        }
    }
}
