create schema bookrentalservice collate utf8_general_ci;

create table book
(
	id int not null
		primary key,
	ISBN char(40) not null,
	Name char(40) null,
	Author char(40) null,
	Price char(20) null,
	Description char(40) null,
	Link char(100) null,
	PicturePath char(100) null,
	IsRentedOut tinyint(1) default 1 not null,
	constraint book_ISBN_uindex
		unique (ISBN)
);

create table user
(
	id int not null
		primary key,
	Name char(20) not null,
	Birthday date not null,
	Gender char(2) null,
	Email char(60) null,
	Telno char(14) null,
	PicturePath char(100) null,
	CanRent tinyint default 1 not null
);

create table bookrental
(
	ID int not null
		primary key,
	UserId int not null,
	BookId int not null,
	RentalDate date null,
	ReturnDate date null,
	isRentOut tinyint(1) default 0 null,
	constraint BookRental_book_ISBN_fk
		foreign key (BookId) references book (id),
	constraint bookrental_user_Name_fk
		foreign key (UserId) references user (id)
);

create table leaveduser
(
	id int null,
	Name char(20) null,
	Birthday date null,
	Gender char(2) null,
	Email char(60) null,
	Telno char(14) null,
	PicturePath char(100) null,
	LeaveDate date null
);


