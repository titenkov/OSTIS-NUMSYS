
/*
-----------------------------------------------------------------------------
This source file is part of OSTIS (Open Semantic Technology for Intelligent Systems)
For the latest info, see http://www.ostis.net

Copyright (c) 2010 OSTIS

OSTIS is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OSTIS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with OSTIS.  If not, see <http://www.gnu.org/licenses/>.
-----------------------------------------------------------------------------
*/


/**
 * @file sc_types.h
 * @brief Definition of sc-types and sc-return codes.
 * @ingroup libsc
 */

#ifndef __LIBSC_SC_TYPES_H_INCLUDED__
#define __LIBSC_SC_TYPES_H_INCLUDED__

/// @addtogroup libsc
/// @{

#if defined(_MSC_VER) && (_MSC_VER <= 1312)
// disable warning for MSVC < 7.1
//	 C++ exception specification ignored except to indicate 
//	a function is not __declspec(nothrow)
#pragma warning(disable:4290)
#endif 


#if defined(WIN32) && defined(libsc_EXPORTS)

#pragma warning(disable:4786)
#pragma warning(disable:4251)

#include <stdlib.h>
#include <stdarg.h>

#elif defined(WIN32)

#pragma warning( disable:4786)
#pragma warning(disable:4251)

#endif 

#include "config.h"

#include <string>

#include <map>
#include <set>
#include <list>
#include <vector>
#include <memory>

/// String type.
typedef std::string sc_string;

/// Empty struct to avoid incorrect casts.
struct sc_addr_ll_struct {};

typedef sc_addr_ll_struct *sc_addr_ll;

#define SCADDR_LL_NIL 0


struct sc_constraint;
class sc_session;
class sc_segment;
class sc_iterator;
class sc_global_addr;

/**
 * @brief Указатель на sc-адрес - основной способ работы с sc-элементами.
 */
typedef sc_global_addr *sc_addr;

#define SCADDR_NIL static_cast<sc_addr>(0) /**< @brief Макрос для указания, что значение типа #sc_addr недействительно. */

typedef int sc_int;
typedef unsigned sc_uint;
typedef short sc_short;
typedef unsigned short sc_ushort;
typedef long sc_long;
typedef unsigned long sc_ulong;
typedef char sc_char;
typedef unsigned char sc_uchar;

typedef sc_char sc_int8;
typedef sc_uchar sc_uint8;

#if (SC_ARCH == i386)
typedef sc_int sc_int32;
typedef sc_uint sc_uint32;
typedef sc_short sc_int16;
typedef sc_ushort sc_uint16;
#else 
#error "Architecture is not defined!"
#endif 

/**
 * @brief Тип sc-элемента.
 */
typedef sc_uint16 sc_type;

#define SC_EMPTY		0 /**< @brief маска отсутствия типа у sc-элемента */

/// @name Битовые маски константности sc-элементов
/// @{
#define SC_CONST		1 /**< @brief константный */
#define SC_VAR 			2 /**< @brief переменный */
#define SC_METAVAR		4 /**< @brief метапеременный */
#define SC_CONSTANCY	(SC_CONST|SC_VAR|SC_METAVAR) /**< @brief маска константности */
/// @}

/// @name Битовые маски нечеткости sc-элементов
/// @{
#define SC_POS			8  /**< @brief позитивный */
#define SC_NEG			16 /**< @brief негативный */
#define SC_FUZ			32 /**< @brief нечеткий */
#define SC_FUZZYNESS    (SC_POS|SC_NEG|SC_FUZ) /**< @brief маска нечеткости */
/// @}

/**
 * @name Битовые маски структурных типов sc-элементов
 */
/// @{
#define SC_UNDF			64  /**< @brief неопределенный тип */
#define SC_ARC			128 /**< @brief sc-дуга */
#define SC_NODE			256 /**< @brief sc-узел */
#define SC_ELMNCLASS	(SC_NODE|SC_ARC|SC_UNDF) /**< @brief маска структурного типа */
/// @}

/// @name Битовые маски постоянства sc-элементов
/// @{
#define SC_TEMPORARY		512  /**< @brief временный */
#define SC_PERMANENT		1024 /**< @brief постоянный */
#define SC_PERMANENCY		(SC_TEMPORARY|SC_PERMANENT) /**< @brief маска постоянства */
/// @}

/// @name Битовые маски призрачности sc-элементов
/// @{
#define SC_PHANTOM		2048 
#define SC_ACTUAL		4096
#define SC_ACTUALITY	(SC_ACTUAL|SC_PHANTOM)
/// @}

// next constants codes modality for phantoms
// factual  - any historized event (that had been actual)
// possible - any that not necessary (enabled by default)
// lost     - any lost event (that would not be actual)
#define SC_FACTUAL		8192  
/*#define SC_POSSIBLE		16384
#define SC_LOST			32768*/

/// @name Битовые маски sc-элемента неопределенного типа различной константности
/// @{
#define SC_U_CONST		(SC_UNDF|SC_CONST)  /**< @brief константный sc-элемент неопределенного типа */
#define SC_U_VAR		(SC_UNDF|SC_VAR) /**< @brief переменный sc-элемент неопределенного типа */
#define SC_U_METAVAR	(SC_UNDF|SC_METAVAR) /**< @brief метапеременный sc-элемент неопределенного типа */
/// @}

/// @name Битовые маски sc-узла различной константности
/// @{
#define SC_N_CONST		(SC_NODE|SC_CONST) /**< @brief константный sc-узел */
#define SC_N_VAR		(SC_NODE|SC_VAR) /**< @brief переменный sc-узел */
#define SC_N_METAVAR		(SC_NODE|SC_METAVAR) /**< @brief метапеременный sc-узел */
/// @}

/// @name Битовые маски sc-дуги различной константности
/// @{
#define SC_A_CONST		(SC_ARC|SC_CONST) /**< @brief константная sc-дуга */
#define SC_A_VAR		(SC_ARC|SC_VAR) /**< @brief переменная sc-дуга */
#define SC_A_METAVAR	(SC_ARC|SC_METAVAR) /**< @brief метапеременная sc-дуга */
/// @}

#define SC_A_PRMN		(SC_PERMANENT|SC_ACTUAL)

#define SC_A_TMPR		(SC_TEMPORARY)

// normal default actuality

#define SC_T_DFLT		(SC_ACTUAL & SC_ACTUALITY)

// default actuality vars & metavars

#define SC_R_DFLT		(SC_PHANTOM & SC_ACTUALITY)

#define SC_XPERMANENCY		(SC_PERMANENCY|SC_FUZ)

#define SC_POOR_MASK		(SC_CONSTANCY|SC_FUZZYNESS|SC_ELMNCLASS)

static inline 
bool __check_sc_type(sc_type val, sc_type mask) 
{
	return val == (val & mask);
}

/**
 * @brief Функция расширение битовой маски, если какие-то признаки не указаны.
 * Функция добавляет к битовой маске @p mask
 * вес биты из @p group, если @p mask не содержит ни одного установленного бита из @p group. 
 */
static inline 
sc_type sc_type_extend_mask_group(sc_type mask, sc_type group) 
{
	return mask |= (mask & group) ? SC_EMPTY : group;
}

/**
 * @brief Расширение битовой маски для всех возможных признаков.
 * @see sc_type_extend_mask_group
 */
static inline 
sc_type sc_type_extend_mask(sc_type mask) 
{
	return sc_type_extend_mask_group(
		sc_type_extend_mask_group(
		sc_type_extend_mask_group(
		sc_type_extend_mask_group(
		sc_type_extend_mask_group(mask, 
		SC_FUZZYNESS), 
		SC_ELMNCLASS), 
		SC_CONSTANCY), 
		SC_PERMANENCY), 
		SC_ACTUALITY);
}

/**
 * @brief Функции проверки включения sc-типа @p val в sc-тип @p mask.
 */
static inline 
bool check_sc_type(sc_type val, sc_type mask) 
{
	return __check_sc_type(val, sc_type_extend_mask(mask));
}

extern unsigned char sc_type_valid_table[];

/**
 * @brief SC-код возврата. 
 * Код возврата функций и методов для работы с sc-памятью.
 */
typedef sc_int sc_retval;

/// @name Возможные sc-коды возврата.
/// @{
#define RV_OK		0	/**< @brief Выполнение прошло успешно. */
#define RV_THEN		RV_OK /**< @brief Переход по ветке then. */
#define RV_ERR_GEN	-1	/**< @brief Произошла неуточняемая ошибка. */
#define RV_ELSE_GEN	1	/**< @brief Неуточняемый переход по ветке else. */
/// @}

/**
 * @brief Проверяет, является ли @p rv ошибочным sc-кодом возврата. 
 */
#define RV_IS_ERR(rv)	(rv<0)

/**
 * @brief Проверяет, является ли @p rv sc-кодом возврата для перехода по ветке else. 
 */
#define RV_IS_ELSE(rv)	(rv>0)

/// Parameter for instantiating #sc_constraint or attaching waits.
/// @see sc_session.attach_wait
union sc_param 
{
	sc_type type;
	sc_addr addr;
	int i;
	sc_segment *seg;
	bool flag;
};

/// @name Predefined stl-containers for #sc_addr_ll.
/// @{

/// std::pair with first and second components as #sc_addr_ll.
typedef std::pair<sc_addr_ll, sc_addr_ll>  ll2ll_pair;

/// std::list, which contains elements of type #sc_addr_ll.
typedef std::list<sc_addr_ll>              ll_list;

/// std::set, which contains elements of type #sc_addr_ll.
typedef std::set<sc_addr_ll>               ll_set;

/// std::map, which maps #sc_addr to #sc_addr_ll.
typedef std::map<sc_addr_ll, sc_addr_ll>   ll2ll_map;

/// std::vector, which contains elements of type #sc_addr_ll.
typedef std::vector<sc_addr_ll>            ll_vector;

/// @}


/// @name Predefined stl-containers for #sc_addr.
/// @{

/// std::pair with first and second components as #sc_addr.
typedef std::pair<sc_addr, sc_addr>  addr2addr_pair;

/// std::list, which contains elements of type #sc_addr.
typedef std::list<sc_addr>           addr_list;

/// std::set, which contains elements of type #sc_addr.
typedef std::set<sc_addr>            addr_set;

/// std::map, which maps #sc_addr to #sc_addr.
typedef std::map<sc_addr, sc_addr>   addr2addr_map;

/// std::vector, which contains elements of type #sc_addr.
typedef std::vector<sc_addr>         addr_vector;

/// std::vector, which contains elements of type #addr2addr_pair.
typedef std::vector<addr2addr_pair>  addr2addr_vector;

/// std::map, which maps #sc_string to #sc_addr.
typedef std::map<sc_string, sc_addr> idtf2addr_map;

/// std::map, which maps #sc_addr to #sc_string.
typedef std::map<sc_addr, sc_string> addr2idtf_map;

/// @}

/**
 * @brief Класс sc-активности.
 */
class LIBSC_API sc_activity 
{
public:
	void *ctx; /**< @brief Контекст */
	bool on_main_stack; 
	bool sched_added; /**< @brief Флаг указвает, добавлена ли активность в планировщик */
	
	sc_activity();
	
	/**
	 * @brief Метод инициализации активности.
	 * @note При корректной инициализации должен возвращать #RV_OK.
	 */
	virtual sc_retval init(sc_addr _this) = 0;
	
	bool is_on_main_stack() 
	{
		return on_main_stack;
	}

	/**
	 * @brief Метод деинициализации активности.
	 */
	virtual void done() = 0;

	/**
	 * @brief Метод активизации активности.
	 * @param s сессия, с которой происходит активация.
	 * @param _this знак данной активности.
	 * @param prm1 первый параметр.
	 * @param prm2 второй параметр.
	 * @param prm3 третий параметр.
	 * @return sc-код возврата.
	 */
	virtual sc_retval activate(sc_session *s, sc_addr _this, sc_addr prm1, sc_addr prm2, sc_addr prm3) = 0;

	virtual ~sc_activity();
};

/// @}

#endif // __LIBSC_SC_TYPES_H_INCLUDED__
