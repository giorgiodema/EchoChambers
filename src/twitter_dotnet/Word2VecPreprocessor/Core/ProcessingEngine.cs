using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using JetBrains.Annotations;
using Newtonsoft.Json;
using Twitter.Models;
using Twitter.Services;

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
        /// <param name="source">The path to the folder that contains the JSON files with all the available tweets</param>
        /// <param name="communitiesPath">The path of the file with the extracted communities (list of user ids)</param>
        /// <param name="destination">The path of the destination folder to save the results</param>
        public static void Process([NotNull] string source, [NotNull] string communitiesPath, [NotNull] string destination)
        {
            // Load the available tweets
            var tweets = new Dictionary<ulong, List<string>>();
            LoadTweets(source, tweets);

            // Load the available communities
            var communities = LoadCommunities(communitiesPath);
        }

        /// <summary>
        /// Loads a collection of tweets from a given path, exploring all subfolders
        /// </summary>
        /// <param name="path">The starting path</param>
        /// <param name="result">The resulting list of tweets</param>
        [CollectionAccess(CollectionAccessType.UpdatedContent)]
        private static void LoadTweets([NotNull] string path, [NotNull] Dictionary<ulong, List<string>> result)
        {
            // Load the tweets in the current directory
            foreach (var file in Directory.EnumerateFiles(path))
            {
                var json = File.ReadAllText(Path.Join(path, file));
                var tweets = JsonConvert.DeserializeObject<IList<Tweet>>(json);
                foreach (var tweet in tweets)
                {
                    // Add the body of the tweet and the retweet too, if present
                    if (result.TryGetValue(tweet.Id, out var list)) list.Add(tweet.Text);
                    else result.Add(tweet.Id, new List<string>(new[] { tweet.Text }));
                    if (tweet.Retweet is Tweet retweet)
                    {
                        if (result.TryGetValue(retweet.Id, out list)) list.Add(retweet.Text);
                        else result.Add(retweet.Id, new List<string>(new[] { retweet.Text }));
                    }
                }
            }

            // Recurse
            foreach (var folder in Directory.EnumerateDirectories(path))
                LoadTweets(Path.Join(path, folder), result);
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
                    yield return line.Split(',').Select(ulong.Parse).ToArray();
        }
    }
}
