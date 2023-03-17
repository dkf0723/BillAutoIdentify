package com.example.demo.model.repository;

import com.example.demo.model.entity.Bill;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface BillRepository extends JpaRepository<Bill, String> {
    List<Bill> findByCheck(String check);
}
