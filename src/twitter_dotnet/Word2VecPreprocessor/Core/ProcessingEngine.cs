using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
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
            // Load the available tweets
            var lookup = EnumerateTweets(options.SourceFolder).Distinct().ToReadOnlyLookup(tweet => tweet.User.Id);

            // Load the available communities and build the dictionaries
            var guid = Guid.NewGuid().ToString("N");
            var communities = new[] { tweets.Keys.ToArray() }.Concat(LoadCommunities(options.CommunitiesFile));
            Parallel.ForEach(communities, (community, _, i) =>
            {
                // Get all the unique tokens for the current community
                var tokens = community.Aggregate(new HashSet<string>(), (s, id) =>
                {
                    s.UnionWith(tweets[id]);
                    return s;
                });

                // Save the dictionary to disk
                var target = Path.Join(options.DestinationFolder, $"{guid}_{i}.ls");
                using (var output = File.CreateText(target))
                    foreach (var token in tokens)
                        output.WriteLine(token);
            });
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
            foreach (var file in Directory.EnumerateFiles(path))
            {
                var json = File.ReadAllText(file);
                var tweets = JsonConvert.DeserializeObject<IList<Tweet>>(json);
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
