using System;
using System.IO;
using System.Threading.Tasks;
using JetBrains.Annotations;
using Newtonsoft.Json;
using Twitter.Services;
using TwitterHydrator.Options;

namespace TwitterHydrator.Core
{
    /// <summary>
    /// A <see langword="class"/> containing code to hydrate a set of tweets
    /// </summary>
    public static class HydratorEngine
    {
        /// <summary>
        /// Processes tweets from a source file and serializes their expanded content to disk
        /// </summary>
        /// <param name="options">The options to use to execute the operations</param>
        /// <param name="service">The <see cref="ITweetsService"/> instance service to use to retrieve tweets</param>
        /// <param name="callback">An optional callback to notify the user of the progress</param>
        public static async Task ProcessAsync(
            [NotNull] HydratorOptions options,
            [NotNull] ITweetsService service,
            [CanBeNull] Action<int, string> callback = null)
        {
            // Create the actual destination folder
            var folder = Path.Join(options.DestinationFolder, Path.GetFileName(options.SourceFile));
            if (Directory.Exists(folder)) throw new InvalidOperationException($"The target directory \"{folder}\" already exists");
            Directory.CreateDirectory(folder);

            // Open the source file and process it
            int total = 0;
            var timestamp = DateTime.MinValue;
            using (var input = File.OpenText(options.SourceFile))
            {
                do
                {
                    // Throttle if needed
                    var difference = DateTime.Now - timestamp;
                    if (difference < TimeSpan.FromSeconds(3)) await Task.Delay(TimeSpan.FromSeconds(3) - difference);
                    timestamp = DateTime.Now;

                    // Read the new lines
                    var lines = input.TakeLines(100);
                    if (lines.Count == 0) return; // EOF
                    callback?.Invoke(total, lines[0]);
                    total += lines.Count;

                    // Load the tweets and save them
                    var tweets = await service.GetTweetsAsync(lines);
                    var json = JsonConvert.SerializeObject(tweets, Formatting.Indented, new JsonSerializerSettings { NullValueHandling = NullValueHandling.Ignore });
                    var target = Path.Join(folder, $"{lines[0]}.json");
                    using (var output = File.CreateText(target))
                        output.Write(json);
                    
                } while (options.Limit == 0 || total < options.Limit);
            }
        }
    }
}
