data = pd.read_csv("./data/OwnInterestRate_data.csv", parse_dates=True, index_col=[0])


def geo_mean(iterable):
    a = np.array(iterable)
    return a.prod() ** (1.0 / len(a))


gCk = geo_mean(data["1992-01-01":]["$g_{I_h}$"].to_list()).round(3)  # Geometric average

initial = 1000
shock_duration=10
df = SolveSFC(model(real=1, gC=gCk, R=0.0), time=initial)
base = model()
SolveSFC(base, time=initial, table=False)

for i in data.index:
    lagged = [key for key in base.solutions[-1].keys()]
    lagged = [i for i in lagged if "__" in i]
    for j in lagged:
        del base.solutions[-1][j]
    base.set_values(base.solutions[-1])
    base.set_values(
        {
            "own": data["Own interest rate"][i],
            "infla": data["Inflation"][i],
            "rm": data["Mortgage interest rate"][i],  # Changed to rm instead of rmo
            "real_data": 1.0,
            "R": 0.0,
            "gC": gCk,
        }
    )
    try:
        SolveSFC(base, time=shock_duration, table=False)
    except Exception as e:
        # print(f'For time = {i}, {e}')
        pass

shock = SFCTable(base)[initial:]
shock["Z/Y"] = shock["Z"] / shock["Y"]
shock["Ih/Y"] = shock["I_h"] / shock["Y"]

base = model()
df = SolveSFC(base, time=1000)
df["Z/Y"] = df["Z"] / df["Y"]
df["Ih/Y"] = df["I_h"] / df["Y"]
df_base = df

shock["TIME"] = [i + 1 for i in range(len(shock.index))]

# First shock
fig, ax = plt.subplots(2, 2, figsize=(19.20, 10.80))

shock["$I_{h}$"] = shock["I_h"]
shock["$I_{f}$"] = shock["I_f"]

shock[["Y", "$I_{h}$", "$I_{f}$"]].pct_change().plot(
    ls="-", lw=3, ax=ax[0, 0], color=("tab:blue", "tab:red", "tab:green")
)
ax[0, 0].axhline(
    y=df_base["g_Z"].iloc[-1], ls="--", lw=1, color="black", label="Baseline"
)
ax[0, 0].ticklabel_format(useOffset=False)
ax[0, 0].set_title("A Selected growth rates")

shock["Z/Y"].plot(ls="-", lw=3, color="black", label="Real data", ax=ax[1, 0])
ax[1, 0].axhline(
    y=df_base["Z/Y"].iloc[-1], ls="--", lw=1.5, color="lightgray", label="Baseline"
)
ax[1, 0].ticklabel_format(useOffset=False)
ax[1, 0].set_title("C Autonomous Expenditure\nShare on GDP ($Z/Y$)")

shock["u"].plot(ls="-", lw=3, color="black", label="Real data", ax=ax[0, 1])
ax[0, 1].axhline(
    y=df_base["u"].iloc[-1], ls="--", lw=1.5, color="lightgray", label="Baseline"
)
ax[0, 1].ticklabel_format(useOffset=False)
ax[0, 1].set_title("B Capacity utilization rate ($u$)")

# shock['h'].plot(ls ='-', lw=3, color = "black", label = "Real data", ax = ax[1,1])
# ax[1,1].axhline(y = df_base['h'].iloc[-1], ls ='--', lw=1.5, color = "lightgray", label = "Baseline")
# ax[1,1].ticklabel_format(useOffset=False)
# ax[1,1].set_title('Marginal propsenty\nto invest ($h$)')

sns.scatterplot(
    y="Z/Y",
    x="u",
    data=shock,
    size="TIME",
    sizes=(1, 100),
    color="black",
    legend=False,
    ax=ax[1, 1],
)

sns.lineplot(
    y="Z/Y", x="u", data=shock, sort=False, color="black", ax=ax[1, 1], legend=False
)
ax[1, 1].set_title(
    "D Share of residential investment and capacity utilization\n(Dots size grow in time)"
)


sns.despine()
plt.tight_layout(rect=[0, 0.03, 0.85, 0.95])
# ax[1,1].legend(loc='center left', bbox_to_anchor=(1.0, 1.25))
# plt.show()
fig.savefig("./figs/Real_Shocks_1.png", dpi=600)


# Second Shock
fig, ax = plt.subplots(2, 2, figsize=(19.20, 10.80))

sns.scatterplot(
    y="Z/Y",
    x="u",
    data=shock,
    size="TIME",
    sizes=(1, 100),
    color="black",
    legend=False,
    ax=ax[0, 0],
)

sns.lineplot(y="Z/Y", x="u", data=shock, sort=False, color="black", ax=ax[0, 0])
ax[0, 0].set_title(
    "A Share of residential investment and capacity utilization\n(Dots size grow in time)"
)

shock["K_k"].plot(ls="-", lw=3, color="black", label="Real data", ax=ax[0, 1])
ax[0, 1].axhline(
    y=df_base["K_k"].iloc[-1], ls="--", lw=1.5, color="lightgray", label="Baseline"
)
ax[0, 1].ticklabel_format(useOffset=False)
ax[0, 1].set_title("B Houses share on\nReal Assets ($K_k$)")

((shock["DN"] * shock["rm"][2:]) / shock["YDk"][2:]).plot(
    ls="-", lw=3, color="black", label="Real data", ax=ax[1, 0]
)
ax[1, 0].axhline(
    y=((df_base["DN"].iloc[-2] * df_base["rm"].iloc[-1]) / df_base["YDk"].iloc[-1]),
    ls="--",
    lw=1.5,
    color="lightgray",
    label="Baseline",
)
ax[1, 0].ticklabel_format(useOffset=False)
ax[1, 0].set_title("C Capitalist Indebtedness\n(as % $YD_k$)")

(shock["Fn"] / shock["K_f"]).plot(
    ls="-", lw=3, color="black", label="Real data", ax=ax[1, 1]
)
ax[1, 1].axhline(
    y=(df_base["Fn"] / df_base["K_f"]).iloc[-1],
    ls="--",
    lw=1.5,
    color="lightgray",
    label="Baseline",
)
ax[1, 1].ticklabel_format(useOffset=False)
ax[1, 1].set_title("D Net profit rate")

sns.despine()
plt.tight_layout(rect=[0, 0.03, 0.85, 0.95])
ax[1, 1].legend(loc="center left", bbox_to_anchor=(1.0, 1.25))
# plt.show()
fig.savefig("./figs/Real_Shocks_2.png", dpi=600)
