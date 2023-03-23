## arabalika Commands
### General  
```/help```  
**@Inputs**  
N/A  
**@Outputs**  
Bot will list the commands.  
  
### Team DPS  
Commands to create an embed featuring Team DPS.  
```/teamdps create```  
**@Inputs**  
title:string, the title of the team  
desc:string (opt), a description of the team and calculations  
**@Outputs**  
Bot will send message.  
Bot will create an embed.  
  
```/teamdps edittext```  
**@Inputs**  
title:string, the title of the team  
desc:string (opt), a description of the team and calculations  
**Outputs**  
Bot will send message.  
Bot wil update embed.  
  
```/teamdps addrotation```  
**@Inputs**  
N/A  
**@Outputs**  
Bot will send message.  
Bot will add rotation to the embed.  
  
```/teamdps addcharacter```  
**@Inputs**  
name:string, the user-declared name of the character  
**@Outputs**  
Bot will send message.  
Bot will add character statistics to the embed.  
  
```/teamdps adddps```  
**@Inputs**  
N/A  
**@Outputs**  
Bot will send message.  
Bot will add a dps section to the embed.  
  
```/teamdps display```  
**@Inputs**  
N/A  
**@Outputs**  
Bot will send Team DPS embed.  
  
### Rotation  
Commands to create a rotation table.  
```/rotation create```  
**@Inputs**  
sec:int, the seconds in the rotation  
col:int (opt), the number of columns in the table.  
**Outputs**  
Bot will create a rotation table.  
Bot will temporarily display rotation.  

```/rotation add```  
**@Inputs**  
desc:string, the description of the action  
interval:string, the time interval during which the action is active, represented either as ```number``` or ```number-number```  
col:int (opt), the column to add the action to  
**@Outputs**  
Bot will add action to rotation.  
Bot will temporarily display rotation.  
  
```/rotation remove```  
**@Inputs**  
interval:string, the time interval during which the action is active, represented either as ```number``` or ```number-number```  
col:int, the column to remove from  
**@Outputs**  
Bot will clear cells in rotation.  
Bot will temporarily display rotation.  

```/rotation addcol```  
**@Inputs**  
col:int, the column to add  
**@Outputs**  
Bot will add a column to the rotation.  
Bot will temporarily display rotation.  

```/rotation removecol```  
**@Inputs**  
col:int, the column to remove  
**@Outputs**  
Bot will remove a column from the rotation.  
Bot will temporarily display rotation.  
  
```/rotation display```  
**@Inputs**  
N/A  
**@Outputs**  
Bot will send the rotation.  
  
### Character  
Commands to create characters. A user may have up to 4 characters.  
```/character create```  
**@Inputs**  
name:string, the unique user-declared name for a character  
**@Outputs**  
Bot will create a character.  
Bot will send message.  

```/character base```  
**@Inputs**  
name:string, the user-declared name for a character  
hp:int (opt), the base HP of the character  
atk:int (opt), the base ATK of the character (with weapon)  
def:int (opt), the base DEF of the character  
em:int (opt), the base Elemental Mastery of the character  
crate:float (opt), the base Critical Rate of the character and weapon; express 24.2% as ```24.2```  
cdmg:float (opt), the base Critical Damage of the character and weapon; express 88.4% as ```88.4```  
er:float (opt), the base Energy Recharge of the character; express 100% as ```100```  
heal:float (opt), the base Healing Bonus of the character; express 0% as ```0```  
ele:float (opt), the base relevant Elemental Damage% of the character; express 0% as ```0```  
**@Outputs**  
Bot will update character base stats.  
Bot will send message.  

```/character main```  
**@Inputs**  
name:string, the user-declared name for a character  
sands:string, the type of sands; atk/hp/def/em/er  
goblet:string, the type of goblet; atk/hp/def/em/ele  
hat:string, the type of hat; atk/hp/def/em/heal  
**@Outputs**  
Bot will update character stats.  
Bot will send message.  
  
```/character subs```  
**@Inputs**  
name:string, the user-declared name for a character  
hp:int (opt), the number of rolls of HP in the artifact subs  
atk:int (opt), the number of rolls of ATK in the artifact subs  
def:int (opt), the number of rolls of DEF in the artifact subs  
em:int (opt), the number of rolls of Elemental Mastery in the artifact subs  
crit:int (opt), the number of rolls of Critical Rate AND Critical Damage in the artifact subs  
er:int (opt), the number of rolls of Energy Recharge in the artifact subs  
**@Outputs**  
Bot will update character stats.  
Bot will send message.  

```/character flat```  
**@Inputs**
name:string, the user-declared name for a character  
hp:int (opt), custom flat amount of HP  
atk:int (opt), custom flat amount of ATK  
def:int (opt), custom flat amount of DEF  
em:int (opt), custom flat amount of EM  
crate:float (opt), custom flat amount of Critical Rate  
cdmg:float (opt), custom flat amount of Critical Damage  
er:float (opt), custom flat amount of Energy Recharge  
heal:float (opt), custom flat amount of Healing Bonus  
ele:float (opt), custom flat amount of relevant Elemental Damage%  
**@Outputs**  
Bot will update character stats.  
Bot will send message.  

```/character energy```  
**@Inputs**  
burst:int, the amount of energy required for Elemental Burst  
onSame:int (opt), the amount of same element on field particles  
offSame:int (opt), the amount of same element off field particles  
onDiff:int (opt), the amount of different element on field particles  
offDiff:int (opt), the amount of different element off field particles  
onNone:int (opt), the amount of no element on field particles  
offNone:int (opt), the amount of no element off field particles  
fixed:int (opt), the amount of fixed energy generated in the rotation  
**@Outputs**  
Bot will calculate and send the amount of energy required to use an Elemental Burst every rotation.  

```/character display```  
**@Inputs**  
N/A  
**@Outputs**  
Bot will display all characters with all calculated stats.  
  
### TEMP COMMANDS  
Commands that may or may not be removed in the future.  
#### Character  
```/character dps```  
**@Inputs**  
value:int, the dps value  
**@Outputs**  
Bot will attach a dps value to the character.  

### FUTURE COMMANDS(?)  
Commands that may or may not be added in the future.  
#### Damage  
Commands to generate damage details  
```/damage add```  
**@Inputs**  
name:string, the user-declared name for a character  
desc:string, a description of the action  
statname:string, the user-declared names for the stats in the format ```stat1``` or ```stat1,stat2,stat3```  
stats:string, the value of the stats of the statnames in the format ```stat1``` or ```stat1,stat2,stat3```  
formula:string, the damage formula is the user-declared names for the stats; format ```stat1*stat2+(1+stat3)```  
**@Outputs**  
Bot sends a message indicating how much damage the character dealt.  
