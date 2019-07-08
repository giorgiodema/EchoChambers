﻿using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
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
            var data = EnumerateTweets(options.SourceFolder).Distinct().ToReadOnlyLookup(tweet => tweet.User.Id);
            var texts = data.Keys.ToDictionary(key => key, key => data[key].Select(tweet => TweetTokenizer.Parse(tweet.Text)).ToArray());

            // Count the occurrences of each word
            var counter = new TokensCounter();
            foreach (var tweets in texts.Values)
                foreach (var tweet in tweets)
                    foreach (var token in tweet)
                        counter.Increment(token);

            // Build the tokens dictionary and save it
            var words = new[] { "<UNK>" }.Concat(counter.Mapping.OrderByDescending(pair => pair.Value).Take(options.Words).Select(pair => pair.Key)).ToArray();
            var lookup = new Dictionary<string, int>();
            foreach (var (word, i) in words.Select((w, i) => (w, i)))
                lookup.Add(word, i);

            // Save the dictionary to disk
            var guid = Guid.NewGuid().ToString("N");
            using (var output = File.CreateText(Path.Join(options.DestinationFolder, $"{guid}_words.ls")))
                foreach (var token in words)
                    output.WriteLine(token);

            // Save the dataset
            using (var output = File.CreateText(Path.Join(options.DestinationFolder, $"{guid}_dataset.ls")))
                foreach (var tweets in texts.Values)
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
    }
}
