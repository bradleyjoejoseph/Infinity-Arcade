# Infinity Network
##### Video Demo: https://www.youtube.com/watch?v=EwcqYN_srsc
##### Description:
Infinite Network is a website for web applications. Some of these applications are games and some are other things. In a real world implementation there would be lots more applications, as more people could work on it.
# Info

## **Welcome, Register and Login**
For the welcome page at first there wasnt a player count and the color scheme was the same, but then I changed it to add more variety and some indication that if the user is signed in the pages would be the dark colors I chose for the website. If not they would have the red yellow black theme for the login, register and welcome page. The register page registers the user and saves their account to the database. The user is then required to login to their account using their username and password.

## **Home, Apps and Settings**
The user is then redirected to the home page. The home page contains the recent apps that the user has visited and the most popular ones by times visited. The user can then use the navbar and click Apps. The app page contains all of the applications that have been created. There is a discover sections where all of the applications are listed. There is a section for apps that you can earn money, a section for games that you can't get money. And and other section. The settings doesn't have much settings apart from the ability to change your bet. If you do when you go into an application that you can earn money in, your bet scales the amount of money you can get and the amount of money you give away.

## **FAQ, Updates, Reviews and Leaderboard**
The user is able to ask questions on the FAQ, this can then be accessed by admins. The updates page is a changelog for updates made to the website. The review page allows the user to rate the website out of 5 stars and critic the website. This page also includes the average rating in stars using all of the ratings of the other users. The leaderboard page contains the names of users and orders them in descending order for the amount of money they have, it also shows the money that the user has along with what place they are in. It only shows the top 100 users with the most amount of money. The current user can see what place they are in as it will show at the top of the leaderboard what their current place is.

## **Admin Pages**
This is only accessable by admins that have to be set in *application.py*. If you are an admin, you are able to delete users, give cash to users, see users details like their id and cash amount (the passwords are hashed). And are able to access the information to the FAQ questions that are asked.

# **The Applications**

## **Infinite Spinner**
Infinite Spinner is a game that you can earn money in it uses python and flask and it is the main source of money on the network, you spin and it is like a luck spin game. The idea of this game came from the popular casino game called [High Society](https://casino-games-review.co.uk/slots/high-society). The spin button reloads the website which automatically spins for you. It requires only a mouse to play. There are also specific rarieties e.g. common, uncommon, rare, epic, legendary. If you get three or more gems you will get £10 for each gem this scales with the bet.

## **Arcade Mathematicians**
Arcade mathematicians is a times table game that you can not earn money in. It is a game that you can play for fun. The times table appears on the screen and you must type in the right answer and it will add to your correct answer number and for wrong answer it will add to your wrong answers number. The idea for this games came from a game played in primary school by small kids called [Times Table Rockstars](https://ttrockstars.com/).

## **Blackjack**
Blackjack is a very popular casino game. In our version you are not able to double your bets in the middle of the game, and gettings 5 cards is not an instant blackjack, the aim is to get 21, if you exceed 21 you lose. If you stand the dealer will draw until they exceed or reach 17. If the dealer has more than you after you stand then you lose, if the dealer hits 21 you lose, if you both have the same number you must hit then stand if you have not exceeded 21 by then.

## **Aim Trainer**
Aim Trainer is a game that you can not earn money in, but you can click targets and add more choose the size of them, choose the radius of them. This game can be used to practice your aim for other games that are FPS's or other shooting games.

## **Chat!**
A very simple chat system that runs on flask. It allows you to connect to other people on the network. It uses SQLite and flask to send and display messages. It shows the time that they sent the message and the user who sent it.

## **CPS Master**
CPS master is a game where you click as fast as you can to see how fast you can click in a second. You can set a certain amount of time like 5 seconds. And click as fast as you can, it will then round it up and you can submit your score and your name will be on the leaderboard if you click fast enough.

## **Poker**
Poker is a implemention of video poker. If you get certain combinations of cards you get money, you choose cards you want to keep, and then draw until you have 5 cards if it comes into the category of one of the combinations then you will get money depending on how much you bet.
