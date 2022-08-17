from unittest import TestCase

import EnumClasses
from OrderBookOneCcyTick import OrderBookOneCcyTick
from Quote import Quote
from QuotesReaderManyCCY import QuotesReaderManyCCY


class TestOrderBookTick(TestCase):
    # This code tests the capabilities of the Level Order Book

    def test_constructor(self):
        test_order_book1 = OrderBookOneCcyTick(EnumClasses.EnumPair.EURUSD)
        test_order_book2 = OrderBookOneCcyTick()
        self.assertEqual(EnumClasses.EnumPair.EURUSD, test_order_book1.get_ccy_pair())
        self.assertEqual(EnumClasses.EnumPair.OTHER, test_order_book2.get_ccy_pair())

    @staticmethod
    def populate_order_book(test_order_book: OrderBookOneCcyTick = None) -> OrderBookOneCcyTick:
        book_ccy_pair = EnumClasses.EnumPair.GBPAUD

        if test_order_book is None:
            test_order_book = OrderBookOneCcyTick(book_ccy_pair)
        else:
            test_order_book.set_ccy_pair(book_ccy_pair)

        quote_str_1 = "N;8157767635857142582;GBP/AUD;30909033292971;1486128909001433;1000000.00;10000.00;0.00;1.62956;B;0"
        quote_str_2 = "N;7668903875291920484;GBP/AUD;30909039049660;1486128909001433;1000000.00;0.00;0.00;1.62954;B;0"
        quote_str_3 = "N;8011963567856449138;GBP/AUD;30909039240037;1486128909001433;1000000.00;50000.00;0.00;1.62948;B;0"
        quote_str_4 = "N;7363795733577871411;GBP/AUD;30909039292231;1486128909001433;1000000.00;0.00;0.00;1.62944;B;0"
        quote_str_5 = "N;8531563110554691444;GBP/AUD;30909039339967;1486128909001433;1000000.00;0.00;0.00;1.62928;B;0"
        quote_str_6 = "N;8175557742412509558;GBP/AUD;30909039385425;1486128909001433;2000000.00;0.00;0.00;1.62928;B;0"
        quote_str_7 = "N;3995656497809207350;GBP/AUD;30909039405229;1486128909001433;1000000.00;0.00;0.00;1.62912;B;0"
        quote_str_8 = "N;8534160972962817592;GBP/AUD;30909039453615;1486128909001433;1000000.00;0.00;0.00;1.62808;B;0"
        quote_str_9 = "N;7292846709437969261;GBP/AUD;30909039506257;1486128909001433;1000000.00;0.00;0.00;1.62788;B;0"
        quote_str_10 = "N;7798089915911466082;GBP/AUD;30909039556827;1486128909001433;5000000.00;0.00;0.00;1.62690;B;0"
        quote_str_11 = "N;7366045616997297003;GBP/AUD;30909039598981;1486128909001433;1000000.00;0.00;0.00;1.63002;S;0"
        quote_str_12 = "N;8100905309745133153;GBP/AUD;30909039647675;1486128909001433;1000000.00;10000.00;0.00;1.63007;S;0"
        quote_str_13 = "N;8446845734467302501;GBP/AUD;30909040034879;1486128909001433;1000000.00;0.00;0.00;1.63008;S;0"
        quote_str_14 = "N;7954876885587092074;GBP/AUD;30909040203626;1486128909001433;1000000.00;50000.00;0.00;1.63009;S;0"
        quote_str_15 = "N;7508754470725510770;GBP/AUD;30909040251663;1486128909001433;2000000.00;0.00;0.00;1.63011;S;0"
        quote_str_16 = "N;4066867490405364331;GBP/AUD;30909040293380;1486128909001433;1000000.00;0.00;0.00;1.63024;S;0"
        quote_str_17 = "N;8516704319123584100;GBP/AUD;30909040333635;1486128909001433;1000000.00;0.00;0.00;1.63040;S;0"
        quote_str_18 = "N;8302512843977353781;GBP/AUD;30909040377430;1486128909001433;1000000.00;0.00;0.00;1.63142;S;0"
        quote_str_19 = "N;7454137351333426543;GBP/AUD;30909040418880;1486128909001433;1000000.00;0.00;0.00;1.63160;S;0"
        quote_str_20 = "N;4063707492950304304;GBP/AUD;30909040456756;1486128909001433;5000000.00;0.00;0.00;1.63284;S;0"

        quote1: Quote = QuotesReaderManyCCY.deserialize_quote(quote_str_1)
        quote2: Quote = QuotesReaderManyCCY.deserialize_quote(quote_str_2)
        quote3: Quote = QuotesReaderManyCCY.deserialize_quote(quote_str_3)
        quote4: Quote = QuotesReaderManyCCY.deserialize_quote(quote_str_4)
        quote5: Quote = QuotesReaderManyCCY.deserialize_quote(quote_str_5)
        quote6: Quote = QuotesReaderManyCCY.deserialize_quote(quote_str_6)
        quote7: Quote = QuotesReaderManyCCY.deserialize_quote(quote_str_7)
        quote8: Quote = QuotesReaderManyCCY.deserialize_quote(quote_str_8)
        quote9: Quote = QuotesReaderManyCCY.deserialize_quote(quote_str_9)
        quote10: Quote = QuotesReaderManyCCY.deserialize_quote(quote_str_10)
        quote11: Quote = QuotesReaderManyCCY.deserialize_quote(quote_str_11)
        quote12: Quote = QuotesReaderManyCCY.deserialize_quote(quote_str_12)
        quote13: Quote = QuotesReaderManyCCY.deserialize_quote(quote_str_13)
        quote14: Quote = QuotesReaderManyCCY.deserialize_quote(quote_str_14)
        quote15: Quote = QuotesReaderManyCCY.deserialize_quote(quote_str_15)
        quote16: Quote = QuotesReaderManyCCY.deserialize_quote(quote_str_16)
        quote17: Quote = QuotesReaderManyCCY.deserialize_quote(quote_str_17)
        quote18: Quote = QuotesReaderManyCCY.deserialize_quote(quote_str_18)
        quote19: Quote = QuotesReaderManyCCY.deserialize_quote(quote_str_19)
        quote20: Quote = QuotesReaderManyCCY.deserialize_quote(quote_str_20)

        test_order_book.incoming_quote(quote1)
        test_order_book.incoming_quote(quote2)
        test_order_book.incoming_quote(quote3)
        test_order_book.incoming_quote(quote4)
        test_order_book.incoming_quote(quote5)
        test_order_book.incoming_quote(quote6)
        test_order_book.incoming_quote(quote7)
        test_order_book.incoming_quote(quote8)
        test_order_book.incoming_quote(quote9)
        test_order_book.incoming_quote(quote10)
        test_order_book.incoming_quote(quote11)
        test_order_book.incoming_quote(quote12)
        test_order_book.incoming_quote(quote13)
        test_order_book.incoming_quote(quote14)
        test_order_book.incoming_quote(quote15)
        test_order_book.incoming_quote(quote16)
        test_order_book.incoming_quote(quote17)
        test_order_book.incoming_quote(quote18)
        test_order_book.incoming_quote(quote19)
        test_order_book.incoming_quote(quote20)

        return test_order_book

    @staticmethod
    def populate_order_book_add_cancels(incoming_book: OrderBookOneCcyTick) -> OrderBookOneCcyTick:
        """
        Adds cancels, modifies for the book
        @param incoming_book:
        @return:
        """
        quote_str_1 = "M;8175557742412509558;GBP/AUD;30909289654019;1486128909065235;2000000.00;0.00;0.00;1.62933"
        quote_str_2 = "M;7508754470725510770;GBP/AUD;30909289686914;1486128909065235;2000000.00;0.00;0.00;1.63014"
        quote_str_3 = "M;8175557742412509558;GBP/AUD;30909308028895;1486128909108005;2000000.00;0.00;0.00;1.62927"
        quote_str_4 = "M;7508754470725510770;GBP/AUD;30909308056806;1486128909108005;2000000.00;0.00;0.00;1.63009"
        quote_str_5 = "M;8175557742412509558;GBP/AUD;30909331661494;1486128909142748;2000000.00;0.00;0.00;1.62936"
        quote_str_6 = "M;7508754470725510770;GBP/AUD;30909331687042;1486128909142748;2000000.00;0.00;0.00;1.63017"
        quote_str_7 = "M;8175557742412509558;GBP/AUD;30909331914798;1486128909142991;2000000.00;0.00;0.00;1.62935"
        quote_str_8 = "M;7508754470725510770;GBP/AUD;30909331928244;1486128909142991;2000000.00;0.00;0.00;1.63016"
        quote_str_9 = "M;8011963567856449138;GBP/AUD;30909341174720;1486128909165099;1000000.00;50000.00;0.00;1.62956"
        quote_str_10 = "M;7954876885587092074;GBP/AUD;30909341191110;1486128909165099;1000000.00;50000.00;0.00;1.63018"
        quote_str_11 = "M;7668903875291920484;GBP/AUD;30909352345064;1486128909186488;1000000.00;0.00;0.00;1.62960"
        quote_str_12 = "M;7366045616997297003;GBP/AUD;30909352371247;1486128909186488;1000000.00;0.00;0.00;1.63007"
        quote_str_13 = "M;7363795733577871411;GBP/AUD;30909352712075;1486128909193231;1000000.00;0.00;0.00;1.62960"
        quote_str_14 = "M;8531563110554691444;GBP/AUD;30909352722478;1486128909193231;1000000.00;0.00;0.00;1.62944"
        quote_str_15 = "M;3995656497809207350;GBP/AUD;30909352734049;1486128909193231;1000000.00;0.00;0.00;1.62928"
        quote_str_16 = "M;7798089915911466082;GBP/AUD;30909352744865;1486128909193231;1000000.00;0.00;0.00;1.62912"
        quote_str_17 = "M;7363795733577871411;GBP/AUD;30909357705615;1486128909231294;1000000.00;0.00;0.00;1.62944"
        quote_str_18 = "M;8531563110554691444;GBP/AUD;30909357717124;1486128909231294;1000000.00;0.00;0.00;1.62928"
        quote_str_19 = "M;3995656497809207350;GBP/AUD;30909357720507;1486128909231294;1000000.00;0.00;0.00;1.62912"
        quote_str_20 = "M;7798089915911466082;GBP/AUD;30909357723239;1486128909231294;5000000.00;0.00;0.00;1.62690"
        quote_str_21 = "M;8534160972962817592;GBP/AUD;30909357863002;1486128909236191;1000000.00;0.00;0.00;1.62889"
        quote_str_22 = "M;7292846709437969261;GBP/AUD;30909357873121;1486128909236191;1000000.00;0.00;0.00;1.62878"
        quote_str_23 = "M;8302512843977353781;GBP/AUD;30909357881186;1486128909236191;1000000.00;0.00;0.00;1.63068"
        quote_str_24 = "M;7454137351333426543;GBP/AUD;30909358122399;1486128909236191;1000000.00;0.00;0.00;1.63077"
        quote_str_25 = "M;7508754470725510770;GBP/AUD;30909358266504;1486128909238595;2000000.00;0.00;0.00;1.63018"
        quote_str_26 = "M;8011963567856449138;GBP/AUD;30909358487596;1486128909240535;1000000.00;50000.00;0.00;1.62952"
        quote_str_27 = "M;7954876885587092074;GBP/AUD;30909358496988;1486128909240535;1000000.00;50000.00;0.00;1.63013"
        quote_str_28 = "N;7380102843177056612;GBP/AUD;30909365068123;1486128909255876;1300000.00;0.00;0.00;1.62939;B;0"
        quote_str_29 = "N;3489782241203153200;GBP/AUD;30909365096555;1486128909255876;1300000.00;0.00;0.00;1.63007;S;0"
        quote_str_30 = "M;8157767635857142582;GBP/AUD;30909368448323;1486128909263195;1000000.00;10000.00;0.00;1.62958"
        quote_str_31 = "M;7363795733577871411;GBP/AUD;30909377816549;1486128909306322;1000000.00;0.00;0.00;1.62960"
        quote_str_32 = "M;8531563110554691444;GBP/AUD;30909377829853;1486128909306322;1000000.00;0.00;0.00;1.62944"
        quote_str_33 = "M;3995656497809207350;GBP/AUD;30909377838336;1486128909306322;1000000.00;0.00;0.00;1.62928"
        quote_str_34 = "M;7798089915911466082;GBP/AUD;30909377846423;1486128909306322;1000000.00;0.00;0.00;1.62912"
        quote_str_35 = "M;3489782241203153200;GBP/AUD;30909377874127;1486128909306996;1300000.00;0.00;0.00;1.63008"
        quote_str_36 = "M;3489782241203153200;GBP/AUD;30909377899263;1486128909307384;1300000.00;0.00;0.00;1.63010"
        quote_str_37 = "M;7363795733577871411;GBP/AUD;30909379764365;1486128909334874;1000000.00;0.00;0.00;1.62944"
        quote_str_38 = "M;8531563110554691444;GBP/AUD;30909379773111;1486128909334874;1000000.00;0.00;0.00;1.62928"
        quote_str_39 = "M;3995656497809207350;GBP/AUD;30909379775092;1486128909334874;1000000.00;0.00;0.00;1.62912"
        quote_str_40 = "M;7798089915911466082;GBP/AUD;30909379776696;1486128909334874;5000000.00;0.00;0.00;1.62690"
        quote_str_41 = "M;7363795733577871411;GBP/AUD;30909396600199;1486128909396581;1000000.00;0.00;0.00;1.62960"
        quote_str_42 = "M;8531563110554691444;GBP/AUD;30909396613293;1486128909396581;1000000.00;0.00;0.00;1.62944"
        quote_str_43 = "M;3995656497809207350;GBP/AUD;30909396622891;1486128909396581;1000000.00;0.00;0.00;1.62928"
        quote_str_44 = "M;7798089915911466082;GBP/AUD;30909396629067;1486128909396581;1000000.00;0.00;0.00;1.62912"
        quote_str_45 = "M;7380102843177056612;GBP/AUD;30909446928512;1486128909446917;1300000.00;0.00;0.00;1.62942"
        quote_str_46 = "M;8175557742412509558;GBP/AUD;30909451569862;1486128909451630;2000000.00;0.00;0.00;1.62939"
        quote_str_47 = "C;4063707492950304304;GBP/AUD;30909468204091;1486128909468111"
        quote_str_48 = "M;8446845734467302501;GBP/AUD;30909468207985;1486128909468111;1000000.00;0.00;0.00;1.63024"
        quote_str_49 = "M;4066867490405364331;GBP/AUD;30909468224259;1486128909468111;1000000.00;0.00;0.00;1.63040"
        quote_str_50 = "M;8516704319123584100;GBP/AUD;30909468227166;1486128909468111;5000000.00;0.00;0.00;1.63284"
        quote_str_51 = "M;7363795733577871411;GBP/AUD;30909506546667;1486128909505347;1000000.00;0.00;0.00;1.62944"
        quote_str_52 = "M;8531563110554691444;GBP/AUD;30909506553958;1486128909505347;1000000.00;0.00;0.00;1.62928"
        quote_str_53 = "M;3995656497809207350;GBP/AUD;30909506556062;1486128909505347;1000000.00;0.00;0.00;1.62912"
        quote_str_54 = "M;7798089915911466082;GBP/AUD;30909506558723;1486128909505347;5000000.00;0.00;0.00;1.62690"
        quote_str_55 = "M;8175557742412509558;GBP/AUD;30909521481421;1486128909517059;2000000.00;0.00;0.00;1.62937"
        quote_str_56 = "M;7508754470725510770;GBP/AUD;30909521494246;1486128909517059;2000000.00;0.00;0.00;1.63017"
        quote_str_57 = "M;7380102843177056612;GBP/AUD;30909521662275;1486128909518595;1300000.00;0.00;0.00;1.62940"
        quote_str_58 = "M;3489782241203153200;GBP/AUD;30909527288565;1486128909527266;1300000.00;0.00;0.00;1.63009"
        quote_str_59 = "M;7363795733577871411;GBP/AUD;30909576138862;1486128909576227;1000000.00;0.00;0.00;1.62960"
        quote_str_60 = "M;8531563110554691444;GBP/AUD;30909576150973;1486128909576227;1000000.00;0.00;0.00;1.62944"
        quote_str_61 = "M;3995656497809207350;GBP/AUD;30909576165582;1486128909576227;1000000.00;0.00;0.00;1.62928"
        quote_str_62 = "M;7798089915911466082;GBP/AUD;30909576169646;1486128909576227;1000000.00;0.00;0.00;1.62912"
        quote_str_63 = "N;4063707492950304304;GBP/AUD;30909601384341;1486128909601254;5000000.00;0.00;0.00;1.63284;S;0"

        quote1 = QuotesReaderManyCCY.deserialize_quote(quote_str_1)
        quote2 = QuotesReaderManyCCY.deserialize_quote(quote_str_2)
        quote3 = QuotesReaderManyCCY.deserialize_quote(quote_str_3)
        quote4 = QuotesReaderManyCCY.deserialize_quote(quote_str_4)
        quote5 = QuotesReaderManyCCY.deserialize_quote(quote_str_5)
        quote6 = QuotesReaderManyCCY.deserialize_quote(quote_str_6)
        quote7 = QuotesReaderManyCCY.deserialize_quote(quote_str_7)
        quote8 = QuotesReaderManyCCY.deserialize_quote(quote_str_8)
        quote9 = QuotesReaderManyCCY.deserialize_quote(quote_str_9)
        quote10 = QuotesReaderManyCCY.deserialize_quote(quote_str_10)
        quote11 = QuotesReaderManyCCY.deserialize_quote(quote_str_11)
        quote12 = QuotesReaderManyCCY.deserialize_quote(quote_str_12)
        quote13 = QuotesReaderManyCCY.deserialize_quote(quote_str_13)
        quote14 = QuotesReaderManyCCY.deserialize_quote(quote_str_14)
        quote15 = QuotesReaderManyCCY.deserialize_quote(quote_str_15)
        quote16 = QuotesReaderManyCCY.deserialize_quote(quote_str_16)
        quote17 = QuotesReaderManyCCY.deserialize_quote(quote_str_17)
        quote18 = QuotesReaderManyCCY.deserialize_quote(quote_str_18)
        quote19 = QuotesReaderManyCCY.deserialize_quote(quote_str_19)
        quote20 = QuotesReaderManyCCY.deserialize_quote(quote_str_20)
        quote21 = QuotesReaderManyCCY.deserialize_quote(quote_str_21)
        quote22 = QuotesReaderManyCCY.deserialize_quote(quote_str_22)
        quote23 = QuotesReaderManyCCY.deserialize_quote(quote_str_23)
        quote24 = QuotesReaderManyCCY.deserialize_quote(quote_str_24)
        quote25 = QuotesReaderManyCCY.deserialize_quote(quote_str_25)
        quote26 = QuotesReaderManyCCY.deserialize_quote(quote_str_26)
        quote27 = QuotesReaderManyCCY.deserialize_quote(quote_str_27)
        quote28 = QuotesReaderManyCCY.deserialize_quote(quote_str_28)
        quote29 = QuotesReaderManyCCY.deserialize_quote(quote_str_29)
        quote30 = QuotesReaderManyCCY.deserialize_quote(quote_str_30)
        quote31 = QuotesReaderManyCCY.deserialize_quote(quote_str_31)
        quote32 = QuotesReaderManyCCY.deserialize_quote(quote_str_32)
        quote33 = QuotesReaderManyCCY.deserialize_quote(quote_str_33)
        quote34 = QuotesReaderManyCCY.deserialize_quote(quote_str_34)
        quote35 = QuotesReaderManyCCY.deserialize_quote(quote_str_35)
        quote36 = QuotesReaderManyCCY.deserialize_quote(quote_str_36)
        quote37 = QuotesReaderManyCCY.deserialize_quote(quote_str_37)
        quote38 = QuotesReaderManyCCY.deserialize_quote(quote_str_38)
        quote39 = QuotesReaderManyCCY.deserialize_quote(quote_str_39)
        quote40 = QuotesReaderManyCCY.deserialize_quote(quote_str_40)
        quote41 = QuotesReaderManyCCY.deserialize_quote(quote_str_41)
        quote42 = QuotesReaderManyCCY.deserialize_quote(quote_str_42)
        quote43 = QuotesReaderManyCCY.deserialize_quote(quote_str_43)
        quote44 = QuotesReaderManyCCY.deserialize_quote(quote_str_44)
        quote45 = QuotesReaderManyCCY.deserialize_quote(quote_str_45)
        quote46 = QuotesReaderManyCCY.deserialize_quote(quote_str_46)
        quote47 = QuotesReaderManyCCY.deserialize_quote(quote_str_47)
        quote48 = QuotesReaderManyCCY.deserialize_quote(quote_str_48)
        quote49 = QuotesReaderManyCCY.deserialize_quote(quote_str_49)
        quote50 = QuotesReaderManyCCY.deserialize_quote(quote_str_50)
        quote51 = QuotesReaderManyCCY.deserialize_quote(quote_str_51)
        quote52 = QuotesReaderManyCCY.deserialize_quote(quote_str_52)
        quote53 = QuotesReaderManyCCY.deserialize_quote(quote_str_53)
        quote54 = QuotesReaderManyCCY.deserialize_quote(quote_str_54)
        quote55 = QuotesReaderManyCCY.deserialize_quote(quote_str_55)
        quote56 = QuotesReaderManyCCY.deserialize_quote(quote_str_56)
        quote57 = QuotesReaderManyCCY.deserialize_quote(quote_str_57)
        quote58 = QuotesReaderManyCCY.deserialize_quote(quote_str_58)
        quote59 = QuotesReaderManyCCY.deserialize_quote(quote_str_59)
        quote60 = QuotesReaderManyCCY.deserialize_quote(quote_str_60)
        quote61 = QuotesReaderManyCCY.deserialize_quote(quote_str_61)
        quote62 = QuotesReaderManyCCY.deserialize_quote(quote_str_62)
        quote63 = QuotesReaderManyCCY.deserialize_quote(quote_str_63)

        incoming_book.incoming_quote(quote1)
        incoming_book.incoming_quote(quote2)
        incoming_book.incoming_quote(quote3)
        incoming_book.incoming_quote(quote4)
        incoming_book.incoming_quote(quote5)
        incoming_book.incoming_quote(quote6)
        incoming_book.incoming_quote(quote7)
        incoming_book.incoming_quote(quote8)
        incoming_book.incoming_quote(quote9)
        incoming_book.incoming_quote(quote10)
        incoming_book.incoming_quote(quote11)
        incoming_book.incoming_quote(quote12)
        incoming_book.incoming_quote(quote13)
        incoming_book.incoming_quote(quote14)
        incoming_book.incoming_quote(quote15)
        incoming_book.incoming_quote(quote16)
        incoming_book.incoming_quote(quote17)
        incoming_book.incoming_quote(quote18)
        incoming_book.incoming_quote(quote19)
        incoming_book.incoming_quote(quote20)
        incoming_book.incoming_quote(quote21)
        incoming_book.incoming_quote(quote22)
        incoming_book.incoming_quote(quote23)
        incoming_book.incoming_quote(quote24)
        incoming_book.incoming_quote(quote25)
        incoming_book.incoming_quote(quote26)
        incoming_book.incoming_quote(quote27)
        incoming_book.incoming_quote(quote28)
        incoming_book.incoming_quote(quote29)
        incoming_book.incoming_quote(quote30)
        incoming_book.incoming_quote(quote31)
        incoming_book.incoming_quote(quote32)
        incoming_book.incoming_quote(quote33)
        incoming_book.incoming_quote(quote34)
        incoming_book.incoming_quote(quote35)
        incoming_book.incoming_quote(quote36)
        incoming_book.incoming_quote(quote37)
        incoming_book.incoming_quote(quote38)
        incoming_book.incoming_quote(quote39)
        incoming_book.incoming_quote(quote40)
        incoming_book.incoming_quote(quote41)
        incoming_book.incoming_quote(quote42)
        incoming_book.incoming_quote(quote43)
        incoming_book.incoming_quote(quote44)
        incoming_book.incoming_quote(quote45)
        incoming_book.incoming_quote(quote46)
        incoming_book.incoming_quote(quote47)
        incoming_book.incoming_quote(quote48)
        incoming_book.incoming_quote(quote49)
        incoming_book.incoming_quote(quote50)
        incoming_book.incoming_quote(quote51)
        incoming_book.incoming_quote(quote52)
        incoming_book.incoming_quote(quote53)
        incoming_book.incoming_quote(quote54)
        incoming_book.incoming_quote(quote55)
        incoming_book.incoming_quote(quote56)
        incoming_book.incoming_quote(quote57)
        incoming_book.incoming_quote(quote58)
        incoming_book.incoming_quote(quote59)
        incoming_book.incoming_quote(quote60)
        incoming_book.incoming_quote(quote61)
        incoming_book.incoming_quote(quote62)
        incoming_book.incoming_quote(quote63)
        return incoming_book

    def test_pair(self):
        test_order_book = TestOrderBookTick.populate_order_book()
        book_ccy_pair = EnumClasses.EnumPair.GBPAUD
        self.assertEqual(book_ccy_pair, test_order_book.get_ccy_pair())

    def test_quotes_count(self):
        test_order_book = TestOrderBookTick.populate_order_book()
        self.assertEqual(20, test_order_book.get_quotes_count())
        self.assertEqual(10, test_order_book.get_quotes_count(True))
        self.assertEqual(10, test_order_book.get_quotes_count(False))

    def test_quotes_count(self):
        test_order_book = TestOrderBookTick.populate_order_book()
        self.assertEqual(20, test_order_book.get_quotes_count())
        self.assertEqual(10, test_order_book.get_quotes_count(True))
        self.assertEqual(10, test_order_book.get_quotes_count(False))
        cm_order_book = TestOrderBookTick.populate_order_book_add_cancels(test_order_book)
        self.assertEqual(22, cm_order_book.get_quotes_count())
        self.assertEqual(11, cm_order_book.get_quotes_count(True))
        self.assertEqual(11, cm_order_book.get_quotes_count(False))

    def test_book_volume(self):
        test_order_book = TestOrderBookTick.populate_order_book()
        self.assertEqual(30000000.0, test_order_book.get_book_volume())
        self.assertEqual(15000000.0, test_order_book.get_book_volume(True))
        self.assertEqual(15000000.0, test_order_book.get_book_volume(False))
        cm_order_book = TestOrderBookTick.populate_order_book_add_cancels(test_order_book)
        self.assertEqual(32600000.0, cm_order_book.get_book_volume())
        self.assertEqual(12300000.0, cm_order_book.get_book_volume(True))
        self.assertEqual(20300000.0, cm_order_book.get_book_volume(False))

    def test_book_vol_sec_ccy(self):
        test_order_book = TestOrderBookTick.populate_order_book()
        self.assertEqual(48893780.0, test_order_book.get_book_volume_in_second_ccy())
        self.assertEqual(24425440.0, test_order_book.get_book_volume_in_second_ccy(True))
        self.assertEqual(24468340.0, test_order_book.get_book_volume_in_second_ccy(False))
        cm_order_book = TestOrderBookTick.populate_order_book_add_cancels(test_order_book)
        self.assertEqual(53160987.0, cm_order_book.get_book_volume_in_second_ccy())
        self.assertEqual(20040770.0, cm_order_book.get_book_volume_in_second_ccy(True))
        self.assertEqual(33120217.0, cm_order_book.get_book_volume_in_second_ccy(False))

    def test_book_snapshot(self):
        test_order_book = TestOrderBookTick.populate_order_book()
        snapshot_all = test_order_book.get_current_snapshot()
        snapshot_bids = test_order_book.get_current_snapshot(True)
        snapshot_offers = test_order_book.get_current_snapshot(False)

        self.assertEqual(20, len(snapshot_all))
        self.assertEqual(10, len(snapshot_bids))
        self.assertEqual(10, len(snapshot_offers))
        for each_bid in snapshot_bids:
            self.assertTrue(each_bid.get_way())
        for each_offer in snapshot_offers:
            self.assertFalse(each_offer.get_way())
        self.assertTrue(snapshot_bids[0].get_id_ecn() != snapshot_bids[1].get_id_ecn())
        self.assertTrue(snapshot_offers[0].get_id_ecn() != snapshot_offers[1].get_id_ecn())

        cm_order_book = TestOrderBookTick.populate_order_book_add_cancels(test_order_book)

        snapshot_all = cm_order_book.get_current_snapshot()
        snapshot_bids = cm_order_book.get_current_snapshot(True)
        snapshot_offers = cm_order_book.get_current_snapshot(False)

        self.assertEqual(22, len(snapshot_all))
        self.assertEqual(11, len(snapshot_bids))
        self.assertEqual(11, len(snapshot_offers))
        for each_bid in snapshot_bids:
            self.assertTrue(each_bid.get_way())
        for each_offer in snapshot_offers:
            self.assertFalse(each_offer.get_way())
        self.assertTrue(snapshot_bids[0].get_id_ecn() != snapshot_bids[1].get_id_ecn())
        self.assertTrue(snapshot_offers[0].get_id_ecn() != snapshot_offers[1].get_id_ecn())


    def test_executed_quotes_for_volume(self):
        test_order_book = TestOrderBookTick.populate_order_book()
        executed_quotes = test_order_book.get_executed_quotes_for_volume(True, 200000.00)

        self.assertEqual(1, len(executed_quotes))
        self.assertEqual(8157767635857142582, executed_quotes[0].get_id_ecn())

        executed_quotes = test_order_book.get_executed_quotes_for_volume(True, 400000.00)

        self.assertEqual(1, len(executed_quotes))
        self.assertEqual(8157767635857142582, executed_quotes[0].get_id_ecn())

        executed_quotes = test_order_book.get_executed_quotes_for_volume(True, 1200000.00)

        self.assertEqual(2, len(executed_quotes))
        self.assertEqual(8157767635857142582, executed_quotes[0].get_id_ecn())
        self.assertEqual(7668903875291920484, executed_quotes[1].get_id_ecn())

        executed_quotes = test_order_book.get_executed_quotes_for_volume(True, 5000000.00)

        self.assertEqual(5, len(executed_quotes))
        self.assertEqual(8157767635857142582, executed_quotes[0].get_id_ecn())
        self.assertEqual(7668903875291920484, executed_quotes[1].get_id_ecn())
        self.assertEqual(8011963567856449138, executed_quotes[2].get_id_ecn())
        self.assertEqual(7363795733577871411, executed_quotes[3].get_id_ecn())
        self.assertEqual(8531563110554691444, executed_quotes[4].get_id_ecn())

        executed_quotes = test_order_book.get_executed_quotes_for_volume(False, 200000.00)

        self.assertEqual(1, len(executed_quotes))
        self.assertEqual(7366045616997297003, executed_quotes[0].get_id_ecn())

        executed_quotes = test_order_book.get_executed_quotes_for_volume(False, 400000.00)

        self.assertEqual(1, len(executed_quotes))
        self.assertEqual(7366045616997297003, executed_quotes[0].get_id_ecn())

        executed_quotes = test_order_book.get_executed_quotes_for_volume(False, 5000000.00)

        self.assertEqual(5, len(executed_quotes))
        self.assertEqual(7366045616997297003, executed_quotes[0].get_id_ecn())
        self.assertEqual(8100905309745133153, executed_quotes[1].get_id_ecn())
        self.assertEqual(8446845734467302501, executed_quotes[2].get_id_ecn())
        self.assertEqual(7954876885587092074, executed_quotes[3].get_id_ecn())
        self.assertEqual(7508754470725510770, executed_quotes[4].get_id_ecn())

    def test_executed_quotes_for_volume_second_ccy(self):
        test_order_book = TestOrderBookTick.populate_order_book()
        executed_quotes = test_order_book.get_executed_quotes_for_volume_in_second_ccy(True, 200000.00 * 1.63000)

        self.assertEqual(1, len(executed_quotes))
        self.assertEqual(8157767635857142582, executed_quotes[0].get_id_ecn())

        executed_quotes = test_order_book.get_executed_quotes_for_volume_in_second_ccy(True, 400000.00 * 1.63000)

        self.assertEqual(1, len(executed_quotes))
        self.assertEqual(8157767635857142582, executed_quotes[0].get_id_ecn())

        executed_quotes = test_order_book.get_executed_quotes_for_volume_in_second_ccy(True, 1200000.00 * 1.63000)

        self.assertEqual(2, len(executed_quotes))
        self.assertEqual(8157767635857142582, executed_quotes[0].get_id_ecn())
        self.assertEqual(7668903875291920484, executed_quotes[1].get_id_ecn())

        executed_quotes = test_order_book.get_executed_quotes_for_volume_in_second_ccy(True, 5000000.00 * 1.63000)

        self.assertEqual(6, len(executed_quotes))
        self.assertEqual(8157767635857142582, executed_quotes[0].get_id_ecn())
        self.assertEqual(7668903875291920484, executed_quotes[1].get_id_ecn())
        self.assertEqual(8011963567856449138, executed_quotes[2].get_id_ecn())
        self.assertEqual(7363795733577871411, executed_quotes[3].get_id_ecn())
        self.assertEqual(8531563110554691444, executed_quotes[4].get_id_ecn())
        self.assertEqual(8175557742412509558, executed_quotes[5].get_id_ecn())

        executed_quotes = test_order_book.get_executed_quotes_for_volume_in_second_ccy(False, 200000.00 * 1.63000)

        self.assertEqual(1, len(executed_quotes))
        self.assertEqual(7366045616997297003, executed_quotes[0].get_id_ecn())

        executed_quotes = test_order_book.get_executed_quotes_for_volume_in_second_ccy(False, 400000.00 * 1.63000)

        self.assertEqual(1, len(executed_quotes))
        self.assertEqual(7366045616997297003, executed_quotes[0].get_id_ecn())

        executed_quotes = test_order_book.get_executed_quotes_for_volume_in_second_ccy(False, 5000000.00 * 1.63000)

        self.assertEqual(5, len(executed_quotes))
        self.assertEqual(7366045616997297003, executed_quotes[0].get_id_ecn())
        self.assertEqual(8100905309745133153, executed_quotes[1].get_id_ecn())
        self.assertEqual(8446845734467302501, executed_quotes[2].get_id_ecn())
        self.assertEqual(7954876885587092074, executed_quotes[3].get_id_ecn())
        self.assertEqual(7508754470725510770, executed_quotes[4].get_id_ecn())

    def test_retrieve_order(self):
        test_order_book = TestOrderBookTick.populate_order_book()
        found_order: Quote = test_order_book.retrieve_order(3995656497809207350)

        self.assertTrue(found_order is not None)
        self.assertEqual(3995656497809207350, found_order.get_id_ecn())

        found_order: Quote = test_order_book.retrieve_order(8446845734467302501)
        self.assertTrue(found_order is not None)
        self.assertEqual(8446845734467302501, found_order.get_id_ecn())

    def test_clear_order_book(self):
        test_order_book = TestOrderBookTick.populate_order_book()
        test_order_book.clear_orderbook()

        self.assertEqual(0, test_order_book.get_quotes_count(True))
        self.assertEqual(0, test_order_book.get_quotes_count(False))

        TestOrderBookTick.populate_order_book(test_order_book)

    def test_get_best_quote(self):
        test_order_book = TestOrderBookTick.populate_order_book()
        best_quote = test_order_book.get_best_quote(True)
        self.assertEqual(1.62956, best_quote.get_price())

        best_quote = test_order_book.get_best_quote(False)
        self.assertEqual(1.63002, best_quote.get_price())

    def test_get_best_price(self):
        test_order_book = TestOrderBookTick.populate_order_book()
        best_quote = test_order_book.get_best_price(True)
        self.assertEqual(1.62956, best_quote)

        best_quote = test_order_book.get_best_price(False)
        self.assertEqual(1.63002, best_quote)