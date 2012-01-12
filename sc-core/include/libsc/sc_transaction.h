
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
 * @file sc_transaction.h
 * @brief Определение мини-транзакции над sc-памятью.
 * @ingroup libsc
 */

#ifndef __LIBSC_SC_TRANSACTION_H_INCLUDED__
#define __LIBSC_SC_TRANSACTION_H_INCLUDED__

#include "libsc.h"

/**
 * @brief Класс мини-транзакции над sc-памятью.
 * Это ненастоящая транзакция. Из ACID данный класс реализует только С, т.е. согласованность.
 * Мини-транзация обрабатывает только генерацию и удаление элементов.
 * @warning Мини-транзакция не поддерживает ссылки.
 */
class LIBSC_API sc_transaction : public sc_session
{
public:
	typedef std::pair<sc_addr,sc_addr> trans_pair;
	typedef std::vector<sc_addr> trans_list;
	typedef std::vector<trans_pair> trans_pair_list;
	typedef std::list<sc_segment*> segment_list;

protected:
	sc_session *host;
	trans_list erased_elems;
	trans_pair_list orig_beg;
	trans_pair_list orig_end;
	trans_list gened_elems;
	segment_list created_segments;
	bool need_rollback;

public:
	
	/**
	 * @param _host сессия, которую необходимо сделать транзакционной.
	 */
	sc_transaction(sc_session *_host) : host(_host), need_rollback(true)
	{
	}

	virtual ~sc_transaction() {}
	void commit();
	void rollback();
	void close() {commit();}

	sc_retval set_beg(sc_addr arc,sc_addr beg);
	sc_retval set_end(sc_addr,sc_addr);
	sc_iterator *create_iterator(sc_constraint *,bool sink);
	sc_addr create_el(sc_segment *,sc_type);
	sc_retval erase_el(sc_addr);
	
	sc_retval activate(sc_addr addr,sc_addr prm1,sc_addr prm2,sc_addr prm3)
	{
		return host->activate(addr,prm1,prm2,prm3);
	}

	bool is_segment_opened(sc_segment *seg) 
	{
		return host->is_segment_opened(seg);
	}

	sc_segment* create_segment(const sc_string &uri)
	{
		sc_segment *rv = host->create_segment(uri);

		if (rv)
			created_segments.push_back(rv);

		return rv;
	}

	sc_segment* open_segment(const sc_string &uri) {return host->open_segment(uri);}
	sc_retval   _stat(const sc_string &uri) {return host->_stat(uri);}
	sc_retval   close_segment(sc_segment *seg) {return host->close_segment(seg);}
	sc_retval   close_segment(const sc_string &uri) {return host->close_segment(uri);}
	sc_retval   unlink(const sc_string &uri) {return host->unlink(uri);}
	sc_retval   rename(const sc_string &oldname, const sc_string &newname) {return host->rename(oldname,newname);}
	sc_retval   mkdir(const sc_string &uri) {return host->mkdir(uri);}
	sc_retval   chdir(const sc_string &uri) {return host->chdir(uri);}
	sc_dir_iterator* search_dir(const sc_string &uri) {return host->search_dir(uri);}
	
	sc_segment *find_segment(const sc_string &uri) 
	{
		return host->find_segment(uri);
	}

	sc_addr get_end(sc_addr addr) {return host->get_end(addr);}
	sc_addr get_beg(sc_addr addr) {return host->get_beg(addr);}
	sc_addr get_end_spin(sc_addr a) {return host->get_end_spin(a);}
	sc_addr get_beg_spin(sc_addr a) {return host->get_beg_spin(a);}

	sc_retval gen3_f_a_f(sc_addr e1,sc_addr *e2,sc_segment *s2,sc_type t2,sc_addr e3) {return host->gen3_f_a_f(e1,e2,s2,t2,e3);}
	sc_retval gen5_f_a_f_a_f(sc_addr e1,sc_addr *e2,sc_segment *s2,sc_type t2,sc_addr e3,sc_addr *e4,sc_segment *s4,sc_type t4,sc_addr e5) {return host->gen5_f_a_f_a_f(e1,e2,s2,t2,e3,e4,s4,t4,e5);}
	sc_retval attach_wait(sc_wait_type type,sc_param *p,int len,sc_wait *w) {return host->attach_wait(type,p,len,w);}
	sc_retval attach_good_wait(sc_wait_type type,sc_param *p,int len,sc_wait *w) {return host->attach_good_wait(type,p,len,w);}
	sc_retval detach_wait(sc_wait *w) {return host->detach_wait(w);}
	sc_type get_type(sc_addr addr) {return host->get_type(addr);}
	sc_retval change_type(sc_addr addr,sc_type type) {return host->change_type(addr,type);}
	sc_string get_idtf(const sc_addr addr) {return host->get_idtf(addr);}
	sc_retval set_idtf(sc_addr addr, const sc_string &idtf) {return host->set_idtf(addr,idtf);}
	sc_retval erase_idtf(sc_addr addr) {return host->erase_idtf(addr);}

	Content get_content(sc_addr addr) {return host->get_content(addr);}
	const Content *get_content_const(sc_addr addr) {return host->get_content_const(addr);}
	sc_retval set_content(sc_addr addr,const Content &c) {return host->set_content(addr,c);}
	sc_retval erase_content(sc_addr addr) {return host->erase_content(addr);}
	bool find_by_content(const Content &content, addr_list &result) { return host->find_by_content(content, result); }

	sc_addr __move_element(sc_addr addr,sc_segment *to) {return host->__move_element(addr,to);}

	sc_retval reimplement(sc_addr addr,sc_activity *new_activity)
	{
		return host->reimplement(addr,new_activity);
	}

	sc_retval get_error() 
	{
		return host->get_error();
	}

	sc_segment *open_segment_spider(const sc_string &uri,bool complete) {return host->open_segment_spider(uri,complete);}
	sc_addr uri2sign(const sc_string &uri) {return host->uri2sign(uri);}
	sc_string sign2uri(sc_addr addr)  {return host->sign2uri(addr);}

	sc_addr find_by_idtf(const sc_string &name,sc_segment *seg)
	{
		return host->find_by_idtf(name,seg);
	}

	int get_in_qnt(sc_addr a) {return host->get_in_qnt(a);}
	int get_out_qnt(sc_addr a) {return host->get_out_qnt(a);}

	sc_session *__fork()
	{
		SC_ABORT();
	}
	bool	erase_el_pre(sc_addr a) {SC_ABORT();}
	sc_retval __erase_el(sc_addr a) {SC_ABORT();}
};

#endif // __LIBSC_SC_TRANSACTION_H_INCLUDED__
