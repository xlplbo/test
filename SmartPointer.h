template <class T>
class CSmartPointer
{
public:
	CSmartPointer();
	CSmartPointer(T* ptr);
	CSmartPointer(CSmartPointer<T>& sp);
	virtual ~CSmartPointer();

	operator bool();
	T*	operator ->();
	CSmartPointer<T>& operator =(CSmartPointer<T>& sp);
	CSmartPointer<T>& operator =(T* p);

protected:
	void	Remove();

	T*	m_ptr;
	unsigned	m_uCount;
};

template <class T>
CSmartPointer<T>::CSmartPointer()
{
	m_ptr = NULL;
	m_uCount = 0;
}

template <class T>
CSmartPointer<T>::CSmartPointer(T* ptr)
{
	m_ptr = ptr;
	m_uCount = 1;
}

template <class T>
CSmartPointer<T>::CSmartPointer(CSmartPointer<T>& sp)
{
	m_ptr = sp.m_ptr;
	m_uCount = sp.m_uCount;
	m_uCount++;
}

template <class T>
CSmartPointer<T>::~CSmartPointer()
{
	Remove();
}

template <class T>
void CSmartPointer<T>::Remove()
{
	m_uCount--;
	if (m_uCount == 0)
	{
		delete(m_ptr);
		m_ptr = NULL;
		m_uCount = 0;
	}
}

template <class T>
CSmartPointer<T>::operator bool()
{
	return (m_ptr != NULL);
}

template <class T>
T*	CSmartPointer<T>::operator->()
{
	_ASSERT(m_ptr);
	return m_ptr;
}

template <class T>
CSmartPointer<T> & CSmartPointer<T>::operator=(CSmartPointer<T>& sp)
{
	if (this == &sp)
	{
		return *this;
	}
	if (m_uCount > 0)
	{
		Remove();
	}
	m_ptr = sp.m_ptr;
	m_uCount = sp.m_uCount;
	m_uCount++;
	return *this;
}

template <class T>
CSmartPointer<T> & CSmartPointer<T>::operator=(T* p)
{
	if (p == m_ptr)
	{
		m_uCount++;
		return *this;
	}
	if (m_uCount > 0)
	{
		Remove();
	}
	m_ptr = p;
	m_uCount = 1;
}
