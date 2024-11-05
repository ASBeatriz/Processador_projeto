library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity addsub is
    Port (
        A     : in  STD_LOGIC_VECTOR(7 downto 0);
        B     : in  STD_LOGIC_VECTOR(7 downto 0);
        operation   : in  STD_LOGIC; -- 0 para adição, 1 para subtração
        clk   : in  STD_LOGIC;
        S     : out STD_LOGIC_VECTOR(7 downto 0);
        Cout  : out STD_LOGIC
    );
end addsub;

architecture Behavioral of addsub is
    signal B_comp : STD_LOGIC_VECTOR(7 downto 0);
    signal C      : STD_LOGIC_VECTOR(8 downto 0); -- Carry para os full adders
    signal S_interno  : STD_LOGIC_VECTOR(7 downto 0);

    component Full_Adder is
        Port (
            A     : in  STD_LOGIC;
            B     : in  STD_LOGIC;
            Cin   : in  STD_LOGIC;
            S     : out STD_LOGIC;
            Cout  : out STD_LOGIC
        );
    end component;

begin
	 U1: Full_Adder port map(A => A(0), B => B_comp(0), Cin => C(0), S => S_interno(0), Cout => C(1));
	 U2: Full_Adder port map(A => A(1), B => B_comp(1), Cin => C(1), S => S_interno(1), Cout => C(2));
	 U3: Full_Adder port map(A => A(2), B => B_comp(2), Cin => C(2), S => S_interno(2), Cout => C(3));
	 U4: Full_Adder port map(A => A(3), B => B_comp(3), Cin => C(3), S => S_interno(3), Cout => C(4));
	 U5: Full_Adder port map(A => A(4), B => B_comp(4), Cin => C(4), S => S_interno(4), Cout => C(5));
	 U6: Full_Adder port map(A => A(5), B => B_comp(5), Cin => C(5), S => S_interno(5), Cout => C(6));
	 U7: Full_Adder port map(A => A(6), B => B_comp(6), Cin => C(6), S => S_interno(6), Cout => C(7));
	 U8: Full_Adder port map(A => A(7), B => B_comp(7), Cin => C(7), S => S_interno(7), Cout => C(8));

    process(clk)
    begin
        if rising_edge(clk) then
            if operation = '1' then
                for i in 0 to 7 loop
                    B_comp(i) <= not B(i);
                end loop;

                C(0) <= '1';
            else
                B_comp <= B;
                C(0) <= '0';
            end if;

            S <= S_interno;
            Cout <= C(8);
        end if;
    end process;

end Behavioral;
