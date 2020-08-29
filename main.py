from argparse import ArgumentParser
import pandas as pd
import numpy as np
import warnings


def shared_budget(filename="data.csv"):
    df = pd.read_csv(filename)
    # Doing some data processing to replace nonconsumer with consumer
    df.rename(columns={"-Consumer": "nonConsumer"}, inplace=True)
    all_consumers = ["Նարեկ", "Վաչիկ", "Մհեր"]
    df.nonConsumer[df.nonConsumer.isna()] = ", ".join(all_consumers)
    df.nonConsumer[df.nonConsumer == "Բոլորը"] = ", ".join(all_consumers)
    df["Buyer "] = df["Buyer "].apply(lambda x: x.strip())  # removing spaces in data
    df["nonConsumer"] = df["nonConsumer"].apply(lambda x: x.strip())
    for consumer in all_consumers:
        df.nonConsumer[df.nonConsumer == consumer] = ", ".join([i for i in all_consumers if i != consumer])
    df = df.rename(columns={"nonConsumer": "consumer"})

    consume_dict = {}
    for consumer in all_consumers:
        consume_dict[consumer] = np.sum(df.Amount / df.consumer.apply(lambda x: len(x.split(", "))
        if consumer in x else None))

    investment_dict = pd.DataFrame.to_dict(df.groupby(by="Buyer ").agg("sum"))["Amount"]
    summary_dict = {key: investment_dict[key] - consume_dict.get(key, 0) for key in investment_dict}
    return summary_dict


if __name__ == "__main__":
    parser = ArgumentParser(description="Calculate shared budget")
    parser.add_argument('--data', '-d', type=str, default='shared_budget.csv', required=True,
                        help='path to the data')
    args = parser.parse_args()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        print(shared_budget(args.data))
