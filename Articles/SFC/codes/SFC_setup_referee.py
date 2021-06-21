base = model()
df = SolveSFC(base, time=1000)
shock = ShockModel(base_model=base, create_function=model(), variable='phi_0', increase=0.005, time = 1000)
clock_plots(shock = shock, filename = 'Clock_1_referee.png', variable='g_Z')
plot_shock(shock = shock, filename = 'Shock_1_referee.png', df=df)
plot_norms(shock = shock, filename = 'Shock_1Norms_referee.png', df=df)
other_plots(shock, df=df)

shock1 = shock.round(decimals = 5).tail(1).transpose().loc['alpha':,:]
shock1.columns = ['$\Delta \phi_0$']
print(shock1.to_latex())

base = model()
df = SolveSFC(base, time=1000)
shock = ShockModel(base_model=base, create_function=model(), variable='omega', increase=-0.01, time = 1000)
df1=shock
clock_plots(shock = shock, filename = 'Clock_2_referee.png', variable='omega')
plot_shock(shock = shock, filename = 'Shock_2_referee.png', df=df)
plot_norms(shock = shock, filename = 'Shock_2Norms_referee.png', df=df)
other_plots(shock, df)
shock2 = shock.round(decimals = 3).tail(1).transpose().loc['alpha':,:]
shock2.columns = ['$\Delta \omega$']
print(shock2.to_latex())

base = model()
df = SolveSFC(base, time=1000)
shock = ShockModel(base_model=base, create_function=model(), variable='rm', increase=0.0025, time = 1000)
df3=shock
shock3 = shock.round(decimals = 3).tail(1).transpose().loc['alpha':,:]
shock3.columns = ['$\Delta rm$']
clock_plots(shock = shock, filename = 'Clock_3_referee.png', variable='rmo')
plot_shock(shock = shock, filename = 'Shock_3_referee.png', df=df)
plot_norms(shock = shock, filename = 'Shock_3Norms_referee.png', df=df)
other_plots(shock, df=df)
print(shock3.to_latex())

base = model()
df = SolveSFC(base, time=1000)
shock = ShockModel(base_model=base, create_function=model(), variable='rm', increase=-0.005, time = 1000)
df3b=shock
shock3b = shock.round(decimals = 3).tail(1).transpose().loc['alpha':,:]
shock3b.columns = ['$\Downarrow rm$']
clock_plots(shock = shock, filename = 'Clock_3b_referee.png', variable='rmo')
plot_shock(shock = shock, filename = 'Shock_3b_referee.png', df=df)
plot_norms(shock = shock, filename = 'Shock_3Normsb_referee.png', df=df)
other_plots(shock, df=df)
print(shock3b.to_latex())

base = model()
df = SolveSFC(base, time=1000)
shock = ShockModel(base_model=base, create_function=model(), variable='infla', increase=0.05, time = 1000)
df2=shock
clock_plots(shock = shock, filename = 'Clock_4_referee.png', variable='infla')
plot_shock(shock = shock, filename = 'Shock_4_referee.png', df=df)
plot_norms(shock = shock, filename = 'Shock_4Norms_referee.png', df=df)
other_plots(shock, df=df)

shock4 = shock.round(decimals = 3).tail(1).transpose().loc['alpha':,:]
shock4.columns = ['$\pi$']
print(shock4.to_latex())

base = model()
df = SolveSFC(base, time=1000)
df = df.round(decimals = 4).tail(1).transpose().loc['alpha':,:]
df.columns = ['Base scenario']

table = pd.merge(left = df, right = shock1, left_index = True, right_index = True)
table = pd.merge(left = table, right = shock2, left_index = True, right_index = True)
table = pd.merge(left = table, right = shock3, left_index = True, right_index = True)
table = pd.merge(left = table, right = shock4, left_index = True, right_index = True)
table = table.loc[:"infla",:] ######### Warning
table.index = [ ######### Warning
    '$\\alpha$',
    '$c_{k}$',
    '$\gamma_F$',
    '$\gamma_u$',
    '$\omega$',
    '$rm$',
    '$\sigma_{l}$',
    '$\sigma_{mo}$',
    '$u_N$',
    '$v$',
    '$\phi_0$',
    '$\phi_1$',
    '$R$',
    '$\pi$'
]
table.to_latex(
    "./tabs/parameters_referee.tex",
    #column_format = 'cccccc',
    escape=False, 
    float_format="{:0.4f}".format,
)

print(table.to_latex(
    escape=False, 
    float_format="{:0.4f}".format,
))

base = model()
df = SolveSFC(base, time=1000)
df["Z/Y"] = df["Z"]/df["Y"]
df_base = df

fig, ax = plt.subplots(2,2, figsize=(19.20,10.80))

df1['Y'].pct_change().plot(ls ='-',lw=3, 
                           #color = "black", 
                           color = "tab:blue",
                           label = "$\\Downarrow \omega$ (Shock 1)", ax = ax[0,0]
)
df2['Y'].pct_change().plot(ls ='-', lw=3, 
                           #color = "darkgray",
                           color = "tab:red",
                           label = "$\\Uparrow \pi$ (Shock 2)", ax = ax[0,0])
df3['Y'].pct_change().plot(ls ='-', lw=3, 
                           #color = "gray", 
                           color = "tab:green",
                           label = "$\\Uparrow r_m$ (Shock 3)", ax = ax[0,0])
#df3b['Y'].pct_change().plot(ls ='-', lw=3, color = "darkgreen", label = "$\\Downarrow r_m$ (Shock 3)", ax = ax[0,0])
ax[0,0].axhline(y = df_base['g_Z'].iloc[-1], ls ='--', lw=1, 
                #color = "lightgray", 
                color = "black",
                label = "Baseline")
ax[0,0].ticklabel_format(useOffset=False)
ax[0,0].set_title('A GDP growth rate ($g$)')

df1['Z/Y'].plot(ls ='-', lw=3, 
                #color = "black", 
                color = "tab:blue",
                label = "$\\Downarrow \omega$ (Shock 1)", ax = ax[0,1])
df2['Z/Y'].plot(ls ='-', lw=3, 
                #color = "darkgray", 
                color = "tab:red",
                label = "$\\Uparrow \pi$ (Shock 2)", ax = ax[0,1])
df3['Z/Y'].plot(ls ='-', lw=3, 
                #color = "gray", 
                color = "tab:green",
                label = "$\\Uparrow r_m$ (Shock 3)", ax = ax[0,1])
#df3b['Z/Y'].plot(ls ='-', lw=3, color = "darkgreen", label = "$\\Downarrow r_m$ (Shock 3)", ax = ax[0,1])
ax[0,1].axhline(y = df_base['Z/Y'].iloc[-1], ls ='--', lw=1.5, 
                #color = "lightgray", 
                color = "black",
                label = "Baseline")
ax[0,1].ticklabel_format(useOffset=False)
ax[0,1].set_title('B Autonomous Expenditure\nShare on GDP ($Z/Y$)')

df1['u'].plot(ls ='-', lw=3, 
              #color = "black", 
              color = "tab:blue", 
              label = "$\\Downarrow \omega$ (Shock 1)", ax = ax[1,0])
df2['u'].plot(ls ='-', lw=3, 
              #color = "darkgray",
              color = "tab:red",  
              label = "$\\Uparrow \pi$ (Shock 2)", ax = ax[1,0])
df3['u'].plot(ls ='-', lw=3, 
              #color = "gray", 
              color = "tab:green", 
              label = "$\\Uparrow r_m$ (Shock 3)", ax = ax[1,0])
#df3b['u'].plot(ls ='-', lw=3, color = "darkgreen", label = "$\\Downarrow r_m$ (Shock 4)", ax = ax[1,0])
ax[1,0].axhline(y = df_base['u'].iloc[-1], ls ='--', lw=1.5, 
                #color = "lightgray",
                color = "black",  
                label = "Baseline")
ax[1,0].ticklabel_format(useOffset=False)
ax[1,0].set_title('C Capacity utilization rate ($u$)')

df1['h'].plot(ls ='-', lw=3, 
              #color = "black", 
              color = "tab:blue", 
              label = "$\\Downarrow \omega$ (Shock 1)", ax = ax[1,1])
df2['h'].plot(ls ='-', lw=3, 
              #color = "darkgray", 
              color = "tab:red", 
              label = "$\\Uparrow \pi$ (Shock 2)", ax = ax[1,1])
df3['h'].plot(ls ='-', lw=3, 
              #color = "gray", 
              color = "tab:green", 
              label = "$\\Uparrow r_m$ (Shock 3)", ax = ax[1,1])
#df3b['h'].plot(ls ='-', lw=3, color = "darkgreen", label = "$\\Downarrow r_m$ (Shock 3)", ax = ax[1,1])
ax[1,1].axhline(y = df_base['h'].iloc[-1], ls ='--', lw=1.5, color = "lightgray", label = "Baseline")
ax[1,1].ticklabel_format(useOffset=False)
ax[1,1].set_title('D Marginal propsenty\nto invest ($h$)')


sns.despine()
plt.tight_layout(rect=[0, 0.03, .85, 0.95])
ax[1,1].legend(loc='center left', bbox_to_anchor=(1.00, 1.25))
#plt.show()
fig.savefig("./figs/Compared_Shocks_1_referee.png", dpi = 300)

base = model()
df = SolveSFC(base, time=1000)
df["Z/Y"] = df["Z"]/df["Y"]
df_base = df

df1["TIME"] = [i+1 for i in range(len(df1.index))]
df2["TIME"] = [i+1 for i in range(len(df2.index))]
df3["TIME"] = [i+1 for i in range(len(df3.index))]
#df3b["TIME"] = [i+1 for i in range(len(df3.index))]

fig, ax = plt.subplots(2,2, figsize=(19.20,10.80))

sns.scatterplot(y = 'Z/Y', x='u', data=df1, size="TIME", sizes = (1,100), color = 'tab:blue', legend=False, ax=ax[0,0])
sns.scatterplot(y = 'Z/Y', x='u', data=df2, size="TIME", sizes = (1,100), color = 'tab:red', legend=False, ax=ax[0,0])
sns.scatterplot(y = 'Z/Y', x='u', data=df3, size="TIME", sizes = (1,100), color = 'tab:green', legend=False, ax=ax[0,0])
#sns.scatterplot(y = 'Z/Y', x='u', data=df3b, size="TIME", sizes = (1,100), color = 'tab:green', legend=False, ax=ax[0,0])

sns.lineplot(y = 'Z/Y', x='u', data=df1, sort=False, color = 'tab:blue', ax=ax[0,0])
sns.lineplot(y = 'Z/Y', x='u', data=df2, sort=False, color = 'tab:red', ax=ax[0,0])
sns.lineplot(y = 'Z/Y', x='u', data=df3, sort=False, color = 'tab:green', ax=ax[0,0])
#sns.lineplot(y = 'Z/Y', x='u', data=df3b, sort=False, color = 'tab:green', ax=ax[0,0])
ax[0,0].set_title('A Share of NCC autonomous expenditures and capacity utilization\n(Dots size grow in time)')

df1['K_k'].plot(ls ='-', lw=3, color = "tab:blue", label = "$\\Downarrow \omega$ (Shock 1)", ax = ax[0,1])
df2['K_k'].plot(ls ='-', lw=3, color = "tab:red", label = "$\\Uparrow \pi$ (Shock 2)", ax = ax[0,1])
df3['K_k'].plot(ls ='-', lw=3, color = "tab:green", label = "$\\Uparrow r_m$ (Shock 3)", ax = ax[0,1])
#df3b['K_k'].plot(ls ='-', lw=3, color = "tab:green", label = "$\\Downarrow r_m$ (Shock 3)", ax = ax[0,1])
ax[0,1].axhline(y = df_base['K_k'].iloc[-1], ls ='--', lw=1.5, color = "black", label = "Baseline")
ax[0,1].ticklabel_format(useOffset=False)
ax[0,1].set_title('B Houses share on\nReal Assets ($K_k$)')

((df1["DN"][1:]*df1["rm"][2:])/df1['K_HD'][2:]).plot(ls ='-', lw=3, color = "tab:blue", label = "$\\Downarrow \omega$ (Shock 1)", ax = ax[1,0])
((df2["DN"][1:]*df2["rm"][2:])/df2['K_HD'][2:]).plot(ls ='-', lw=3, color = "tab:red", label = "$\\Uparrow \pi$ (Shock 2)", ax = ax[1,0])
((df3["DN"]*df3["rm"])[1:]/df3['K_f'][1:]).plot(ls ='-', lw=3, color = "tab:green", label = "$\\Uparrow r_m$ (Shock 3)", ax = ax[1,0])
#((df3b["MO"]*df3b["rmo"][1:] + df3b["Lk"]*df3b["rl"][1:] - df3b["M"]*df3b["rl"][1:])/df3b['K_HD'][1:]).plot(ls ='-', lw=3, color = "tab:green", label = "$\\Uparrow r_m$ (Shock 3)", ax = ax[1,0])
ax[1,0].axhline(y = ((df_base["DN"].iloc[-1]*df_base["rm"].iloc[-1])/df_base['K_HD'].iloc[-1]), ls ='--', lw=1.5, color = "black", label = "Baseline")
ax[1,0].ticklabel_format(useOffset=False)
ax[1,0].set_title('C Capitalist Indebtedness\n(as % $K_{HD}$)')

(df1['Fn']/df1['K_f']).plot(ls ='-', lw=3, color = "tab:blue", label = "$\\Downarrow \omega$ (Shock 1)", ax = ax[1,1])
(df2['Fn']/df2['K_f']).plot(ls ='-', lw=3, color = "tab:red", label = "$\\Uparrow \pi$ (Shock 2)", ax = ax[1,1])
(df3['Fn']/df3['K_f']).plot(ls ='-', lw=3, color = "tab:green", label = "$\\Uparrow r_m$ (Shock 3)", ax = ax[1,1])
#(df3b['Fn']/df3b['K_f']).plot(ls ='-', lw=3, color = "tab:green", label = "$\\Downarrow r_m$ (Shock 3)", ax = ax[1,1])
ax[1,1].axhline(y = (df_base['Fn']/df_base['K_f']).iloc[-1], ls ='--', lw=1.5, color = "black", label = "Baseline")
ax[1,1].ticklabel_format(useOffset=False)
ax[1,1].set_title('D Net profit rate')

sns.despine()
plt.tight_layout(rect=[0, 0.03, .85, 0.95])
ax[1,1].legend(loc='center left', bbox_to_anchor=(1.0, 1.25))
#plt.show()
fig.savefig("./figs/Compared_Shocks_2_referee.png", dpi = 600)
