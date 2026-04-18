\documentclass[11pt]{article}
\usepackage{geometry}
\geometry{letterpaper, margin=1in}
\usepackage{circuitikz}
\usepackage{amsmath}

\begin{document}

\noindent \textbf{Problem 1: Sensor interfaces, loading, frequency response}

\vspace{1.5em}
\begin{center}
\begin{circuitikz}[american, thick]
    % 1. 左侧：Photodiode linear model
    \draw (0,0) to[I, l=$i_d$] (0,3);
    \draw (2,0) to[R, l=$r_d$, *-*] (2,3);
    \draw (4,0) to[C, l=$c_j$, *-*] (4,3);
    \draw (0,3) -- (4,3);
    \draw (0,0) -- (4,0);
    \draw[dashed] (-1, -0.5) rectangle (4.8, 3.5);
    \node[align=center] at (1.9, 4.1) {\textit{photodiode} \\ \textit{linear model}};

    % 2. 中间：连接线、电流电压标记与接地
    \draw (4.8,3) to[short, i=$i_{in}$] (6.2,3);
    \draw (4,3) -- (4.8,3);   
    \draw (6.2,3) -- (7.5,3); 
    \draw (4,0) -- (7.5,0);
    \filldraw (5.5,0) circle (1.5pt);
    \node[ground] at (5.5,0) {};
    \node at (5.5, 2.5) {$+$};
    \node at (5.5, 1.5) {$v_{in}$};
    \node at (5.5, 0.5) {$-$};

    % 3. 右侧：Circuit
    \draw (7.5,3) to[R, l_=$R_{in}$] (7.5,0);
    \draw[dashed] (6.2, -0.5) rectangle (8.8, 3.5);
    \node at (7.5, 4.1) {\textit{circuit}};
\end{circuitikz}
\end{center}
\vspace{1.5em}

Photodiodes, which are used to convert light into electric current, are typically modeled as shown above, as current sources in parallel with a ``small-signal'' resistance and a junction capacitance. The resistance and capacitance exhibited by the diode are in general nonlinear, such that the linear approximations shown here are valid only over a narrow range of currents/voltages. For the purposes of analysis and design, we treat them as simple passive components $r_d$ and $c_j$.

\vspace{1.5em}
\noindent \underline{\textit{Analysis}}
\vspace{1em}

\noindent \textbf{a)} Determine an expression for the the transfer function $\frac{V_{in}}{I_d}(s)$ in terms of $r_d$, $c_j$, and $R_{in}$.

\vspace{1em}
\noindent \textbf{b)} Let $r_d = 10k\Omega$, $c_j = 1pF$, and $R_{in} = 1k\Omega$. Use \textit{Python} to plot the magnitude and phase of the transfer function $\frac{V_{in}}{I_d}(s)$. What is the 3db-bandwidth ($\omega_0 = 1/\tau$) of the magnitude response?

\vspace{1em}
\noindent \textit{Please show your work}

\vspace{2.5em}
\noindent \underline{\textit{Design}}
\vspace{1em}

\noindent \textbf{c)} For the values of $r_d$ and $R_{in}$ in \textit{Part b}, by what percentage is the diode current attenuated due to loading at DC ($f = 0$)? That is, what percentage of $i_d$ is ``lost'' due to the finite output resistance ($r_d$) of the diode?

\vspace{1em}
\noindent Calculate a new value of $R_{in}$ that results in only 0.1\% attenuation of the diode current at DC.

\vspace{1em}
\noindent \textit{Note: For DC calculations you can ignore the presence of $c_j$, because its impedance magnitude $\left| \frac{1}{j\omega c_j} \right|$ is infinite.}

\vspace{1em}
\noindent \textbf{d)} Using the value of $R_{in}$ calculated in \textit{Part c}, use \textit{Python} to plot the magnitude and phase of the transfer function. Build the circuit in SPICE and run an AC simulation. Ensure that the magnitude/phase responses agree with those from your analytical (\textit{Python}) model.

\vspace{2.5em}
\noindent \textit{Suggestion: Try using Latex for displaying mathematical expressions and equations. One nice feature of Jupyter Notebooks is its ability to incorporate both code and ``markup,'' used for formatting text, into the same document. Some examples of Latex are given above in the problem descriptions. You can press Return or double click a cell to see the markup, then use Shift-Return to view the formatted version. Here are a few more examples:}

\begin{align*}
    j &= \sqrt{-1} \\
    V &= IR \\
    I_C &= C \cdot \frac{dV}{dt}
\end{align*}

\vspace{1.5em}
\noindent \texttt{In [ ]:}

\end{document}