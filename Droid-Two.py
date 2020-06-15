####importation
import random
import sys
import gensim
import csv

#### load 3go file


model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

####fin load
#### init func
you=0
she_he_it=0
we_i=0
formule_aurevoir=[]
interro_question_bool=False
badword=False
goodword=False
dominant_operator_bool=False
#### fin init

#### definition func
def reco_question(input_reponse):
    if "?" in input_reponse:
        return 1
    else:
        for mots in input_reponse:
            for lettres in mots:
                if lettres=="?":
                    return 1

def badword_func(input_reponse):
    wordlist=open("badwords.txt","r")
    wordlist_data=wordlist.read()
    wordlist.close()
    for mots in wordlist_data.split(" "):
        mots=mots.upper()
        for mot in input_reponse:
            if mots==mot:
                return 1,mot
    return False,0

def goodword_func(input_reponse):
    wordlist=open("goodwords.txt",'r')
    wordlist_data=wordlist.read()
    wordlist.close()
    for mots in wordlist_data.split("\n"):
        mots=mots.upper()
        for mot in input_reponse:
            if mots==mot:
                return 1,mot
    return False,0

def dont_say_that(mot):
    if mot=="me":
        var="Don't say that ..."
    elif mot=="autres":
        var="That's not cool for them/him/her !"
    return var

def raw(input_reponse):
    mot=""
    final=""
    var=input_reponse
    if var[-1]=="?" or var[-1]=="!" or var[-1]=="." or var[-1]=="," or var[-1]==";":
            del var[-1]
    for mot in input_reponse:
        final+=mot

    print(final)

    print("Checking raw")
    p=open("reponses.csv",'r')
    data=p.read()
    p.close()
    for lignes in data.split("\n"):
        final_final=""
        ligne_mots=lignes.split(",")
        final2=ligne_mots[0]
        final3=final2.split(" ")
        for lettre in final3:
            final_final+=lettre
        if final_final==final:
            print("raw=True")
            final_final=""
            return ligne_mots[1],True
    final_final=""
    return "",False

def process_database(input_reponse,model):
    mini=10
    mot_temp=""
    print(input_reponse)
    """raw,bool_raw=raw(input_reponse)
    if bool_raw==True:
        return raw"""
    r=open('reponses.csv','r')
    data=r.read()
    r.close()
    for words in data.split("\n"):
        part=words.split(",")
        part_official=part[0]

        compare1=part_official
        if compare1!="":
            distance = model.wmdistance(compare1, input_reponse)
            #print ('distance '+compare1+"-"+input_reponse+" ="+'%.3f' % distance)
            if distance<mini:
                mot_temp=part[1]
                mini=distance
    return mot_temp

def generic_reply(word):
    """return reponse"""
    print("generic method : "+word)
    if word=="bad":
        reponses_bad=["You're trash","Why ?","You're talking to me ?","Why are you bullying me :'(","That's not cool","Be polite please !"]
        random_number_4=random.randint(0,4)
        reponses_bad_final=reponses_bad[random_number_4]
    return reponses_bad_final

def reply_bad(operator):
    """return reponse"""
    print("reply bad with operator :"+operator)
    if operator=="you-you're":
        reply=generic_reply("bad")
    elif operator=="she-he-it-they-she's-he's-it's-they're":
        reply=dont_say_that("autres")
    elif operator=="we-i-we're-i'm":
        reply=dont_say_that('me')
    else:
        reply="Error"
    return reply

def reply_good(operator):
    """return reponse"""
    print("reply good with operator :"+operator)
    return 1

def write(question, reponse):
    with open("reponses.csv","a") as csv_file:
        colonnes= ['question','reponse']
        writer=csv.DictWriter(csv_file, fieldnames=colonnes)
        writer.writerow({'question':question, "reponse":reponse})

#### Fin def func

#### Starting
print("Bot >>Hi, How are ya ?")
reponse=input("Usr >>")
reponse=reponse.upper()
classic=["FINE","GOOD"]
classic2=["HELLO","HI"]
random_number2=random.randint(0,1)
random_salutation=classic2[random_number2].lower()


if "?" in reponse.split(" "):
    print("Bot >>I'm good, thx for asking !")
elif classic[0]==reponse or classic[1]==reponse:
    print("Bot >>cool !")
elif "FINE" in reponse:
    print("Bot >>Oh, cool :)")
elif "BAD" in reponse.split(" "):
    print("Bot >>uh...Sorry for asking you :(")
else:
    print("Uhh... OK")


#### starting end

#### engagement conversation
formule_engager=["What brings you here ?","What's the matter ?","How did you land here ?","My name is Droid One v2 but you can call me Droid if you want :)","What are you doing here ?","Long time no see !"]
random_number=random.randint(0,5)
formule_random=formule_engager[random_number]
print("Bot >>"+formule_random)
#### fin engagement

#### entrée utilisateur
while True :
    reponse=input("Usr >>")
    print("\n")
    reponse=reponse.upper()
    if reponse == "EXIT":
        formule_aurevoir=['Adios','Bye','Goodbye','See you',"See Ya"]
        random_number_3=random.randint(0,4)
        formule_aurevoir_random=formule_aurevoir[random_number_3]
        print("Bot >>"+formule_aurevoir_random)
        sys.exit()
#### fin entrée utilisateur

#### reconnaissance I/you/she/he/we/they
    reponse_splitted=reponse.split(" ")
    for mot in reponse_splitted:
        if mot=='YOU' or mot=="YOU'RE":
            you+=1
        if mot=='WE' or mot=='I' or mot=="I'M" or mot=="WE'RE":
            we_i+=1
        if mot=='SHE' or mot=='HE' or mot=='IT' or mot=='THEY' or mot=="SHE'S" or mot=="HE'S" or mot=="IT'S" or mot=="THEY'RE":
            she_he_it+=1

    print("she/he/it/they :"+str(she_he_it),"we/I :"+str(we_i),"you :"+str(you))
    if she_he_it>we_i and she_he_it>you:
        dominant_operator="she-he-it-they-she's-he's-it's-they're"
        dominant_operator_bool=True

    elif we_i>she_he_it and we_i>you:
        dominant_operator="we-i-we're-i'm"
        dominant_operator_bool=True

    elif you>she_he_it and you>we_i:
        dominant_operator="you-you're"
        dominant_operator_bool=True

    elif you==we_i and you==she_he_it:
        dominant_operator_bool=False    

#### fin reco

#### reconnaissance question
    interro_question=reco_question(reponse_splitted)
    if interro_question==1:
        interro_question_bool=True
    if interro_question_bool==True:
        print("C'est une question !")
#### fin reco question

#### reco bad word
    badword_out,badword_sortie=badword_func(reponse_splitted)
    if badword_out==1:
        badword=True
        temp_badword=badword_sortie
        print("Badword :(")
    else:
        print("No badwords :)")
#### fin reco bad word

#### reco good word
    goodword_out,goodword_sortie=goodword_func(reponse_splitted)
    if goodword_out==1:
        goodword=True
        print("Good Word :)")
        temp_goodword=goodword_sortie
    else:
        print("No Good Word :|")
#### fin reco good word

#### processing
    if interro_question_bool==True:
        if dominant_operator_bool==True:
            bot_reponse=process_database(reponse,model)
        else:
            bot_reponse=process_database(reponse,model)

    elif goodword==False and badword==True:
        if dominant_operator_bool==True:
            bot_reponse=reply_bad(dominant_operator)
        else:
            bot_reponse=generic_reply("bad")

    elif badword==False and goodword==True:
        if dominant_operator_bool==True:
            bot_reponse=reply_good(dominant_operator)
        else:
            bot_reponse=generic_reply("good")

    elif (badword==True and goodword==True) or (badword==False and goodword==False):
        if dominant_operator_bool==True:
            bot_reponse=process_database(reponse,model)
        else:
            bot_reponse=process_database(reponse,model)
        


    if reponse=="YES" or reponse=="NO" or reponse=="YEP" or reponse=="NOPE":
        liste_yes_no=["Ok","Cool","Good","Fine","Bueno !"]
        random_number_4=random.randint(0,4)
        bot_reponse=liste_yes_no[random_number_4]
##### processing 

#### reponse bot
    print("Bot >>"+str(bot_reponse)+"\n")
#### fin reponse bot

#### reinit var
    dominant_operator_bool=False
    interro_question_bool=False
    goodword=False
    badword=False
    you=0
    she_he_it=0
    we_i=0
    temp_badword=""
    temp_goodword=""
#### fin reinit var
