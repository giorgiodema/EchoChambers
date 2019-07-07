using System;
using System.Threading.Tasks;
using CommandLine;
using JetBrains.Annotations;
using Twitter;
using Twitter.Models.OAuth;
using TwitterHydrator.Core;
using TwitterHydrator.Enums;
using TwitterHydrator.Options;

namespace TwitterHydrator
{
    public sealed class Program
    {
        /// <summary>
        /// The path of the JSON file containing the API keys to use
        /// </summary>
        private const string ApiKeysPath = @"C:\Users\Sergi\Documents\WIR\twitter_api_keys.json";

        /// <summary>
        /// A <see cref="TaskCompletionSource{TResult}"/> instance used to track the completion of the user requested operations
        /// </summary>
        [NotNull]
        private static readonly TaskCompletionSource<object> Tcs = new TaskCompletionSource<object>();

        public static async Task Main(string[] args)
        {
            // Parse the arguments and execute the requested operations
            new Parser()
                .ParseArguments<HydratorOptions>(args)
                .WithParsed(async options =>
                {
                    var apiKeys = OAuth2ClientInfo.LoadFromFile(ApiKeysPath);
                    var service = TwitterServiceFactory.GetTweetsService(apiKeys.ApplicationName, apiKeys.AccessToken);
                    await HydratorEngine.ProcessAsync(options, service, (i, id) => ConsoleHelper.Write(MessageType.Info, $"[i]: {id}"));
                    Tcs.SetResult(null);
                })
                .WithNotParsed(errors =>
                {
                    foreach (var error in errors)
                        ConsoleHelper.Write(MessageType.Error, error.ToString());
                    Tcs.SetResult(null);
                });

            // Wait for the completion of the pending operations
            await Tcs.Task;
            Console.ReadKey();
        }
    }
}
