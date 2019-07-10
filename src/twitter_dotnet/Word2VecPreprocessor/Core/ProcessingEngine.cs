using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Helpers.UI;
using JetBrains.Annotations;
using Newtonsoft.Json;
using Twitter.Models;
using Word2VecPreprocessor.Extensions;
using Word2VecPreprocessor.Options;

namespace Word2VecPreprocessor.Core
{
    /// <summary>
    /// A <see langword="class"/> containing code to preprocess a series of tweets data
    /// </summary>
    public static class ProcessingEngine
    {
        /// <summary>
        /// Processes the incoming twitter data
        /// </summary>
        /// <param name="options">The options to use to execute the operations</param>
        public static void Process([NotNull] ProcessingOptions options)
        {
            // Load the tweets as a collection of tokens
            ConsoleHelper.Write(MessageType.Info, "Reading tweets...");
            var data = EnumerateTweets(options.SourceFolder).Distinct().ToReadOnlyLookup(tweet => tweet.User.Id);
            var texts = data.Keys.ToDictionary(key => key, key => data[key].Select(tweet => TweetTokenizer.Parse(tweet.Text)).ToArray());
            ConsoleHelper.Write(MessageType.Info, $"{data.Values.Aggregate(0, (s, l) => s + l.Count)} tweets loaded");

            // Count the occurrences of each word
            ConsoleHelper.Write(MessageType.Info, "Counting tokens...");
            var counter = new TokensCounter();
            foreach (var tweets in texts.Values)
                foreach (var tweet in tweets)
                    foreach (var token in tweet)
                        counter.Increment(token);
            ConsoleHelper.Write(MessageType.Info, $"{counter.Mapping.Count} total tokens");

            // Build the tokens dictionary and save it
            ConsoleHelper.Write(MessageType.Info, "Building sorted tokens mapping...");
            var words = new[] { "<UNK>" }.Concat(counter.Mapping.OrderByDescending(pair => pair.Value).Take(options.Words).Select(pair => pair.Key)).ToArray();
            var lookup = new Dictionary<string, int>();
            foreach (var (word, i) in words.Select((w, i) => (w, i)))
                lookup.Add(word, i);

            // Save the dictionary to disk
            ConsoleHelper.Write(MessageType.Info, "Saving tokens dictionary to disk...");
            var guid = Guid.NewGuid().ToString("N");
            using (var output = File.CreateText(Path.Join(options.DestinationFolder, $"{guid}_words.ls")))
                foreach (var token in words)
                    output.WriteLine($"{(counter.Mapping.TryGetValue(token, out var count) ? count : -1)} {token}");

            // Save the dataset
            ConsoleHelper.Write(MessageType.Info, "Saving dataset...");
            using (var output = File.CreateText(Path.Join(options.DestinationFolder, $"{guid}_dataset.ls")))
                foreach (var tweets in texts.Values)
                    foreach (var tweet in tweets)
                        output.WriteLine(string.Join(' ', tweet.Select(token => lookup.TryGetValue(token, out int i) ? i : 0)));

            // Save the datasets of the specific communities
            ConsoleHelper.Write(MessageType.Info, "Saving community datasets...");
            foreach (var community in LoadCommunities(options.CommunitiesFile).Take(options.CommunitiesLimit).Select((c, i) => (Users: c, Id: i)))
                using (var output = File.CreateText(Path.Join(options.DestinationFolder, $"{guid}_dataset_{community.Id}.ls")))
                    foreach (var tweets in community.Users.Select(id => texts[id]))
                        foreach (var tweet in tweets)
                            output.WriteLine(string.Join(' ', tweet.Select(token => lookup.TryGetValue(token, out int i) ? i : 0)));
        }

        /// <summary>
        /// Enumerates over all the existing tweets in a specified directory, including all subfolders as well
        /// </summary>
        /// <param name="path">The path of the directory to explore</param>
        [Pure]
        [NotNull, ItemNotNull]
        private static IEnumerable<Tweet> EnumerateTweets([NotNull] string path)
        {
            // Load the tweets in the current directory
            foreach (var tweets in Directory.EnumerateFiles(path).AsParallel().Select(file =>
            {
                var json = File.ReadAllText(file);
                return JsonConvert.DeserializeObject<IList<Tweet>>(json);
            }))
            {
                // For each tweet, return the tweet and the original status, if present
                foreach (var tweet in tweets)
                {
                    yield return tweet;
                    if (tweet.Retweet is Tweet retweet) yield return retweet;
                }
            }

            // Recurse
            foreach (var folder in Directory.EnumerateDirectories(path))
                foreach (var tweet in EnumerateTweets(folder))
                    yield return tweet;
        }

        /// <summary>
        /// Loads the list of user ids for the available communities
        /// </summary>
        /// <param name="path">The path of the CSV file with the list of user ids</param>
        [NotNull, ItemNotNull]
        [Pure]
        private static IEnumerable<IReadOnlyList<ulong>> LoadCommunities([NotNull] string path)
        {
            using (var reader = File.OpenText(path))
                while (reader.ReadLine() is string line)
                    yield return line.Split(',', StringSplitOptions.RemoveEmptyEntries).Select(ulong.Parse).ToArray();
        }
    }
}
